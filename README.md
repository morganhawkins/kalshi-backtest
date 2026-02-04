# Kalshi Backtesting Framework

A framework for backtesting binary option strategies on the Kalshi exchange. The project provides multiple pricing models with Greek calculations, delta hedging agents, and infrastructure for handling irregularly sampled market data.

## Overview

This framework enables:

- **Pricing** binary and event-based derivative contracts using multiple model families
- **Computing Greeks** (delta, gamma, vega, theta) for risk management
- **Delta hedging** derivative positions by dynamically trading the underlying
- **Backtesting** hedging strategies on historical market data with irregular timestamps

## Available Models

All models inherit from `BaseModel` and implement pricing with implied volatility and Greek calculations.

### Geometric Brownian Motion (GBM)

Located in `src/models/geom_bm/`

**GBMStepModel** - Prices barrier/step contracts assuming the underlying follows geometric Brownian motion with log-normal returns. Uses closed-form Black-Scholes-style formulas with the error function for cumulative normal distribution.

- Parameters: `sigma` (volatility), `mu` (drift)
- Terminal payoff: 1 if underlying >= strike at expiration, else 0

**GBMRangeModel** - Prices range contracts as a spread between two strikes. Useful for "will the underlying be between X and Y?" style bets.

### Cauchy Distribution

Located in `src/models/geom_cauchy/`

**CauchyStepModel** and **CauchyRangeModel** - Alternative to GBM that assumes log returns follow a Cauchy distribution instead of normal. Better captures fat tails and extreme market moves.

- Parameters: `scale` (volatility analog), `loc` (location/drift)
- Uses arctangent instead of error function for CDFs
- Better suited for volatile or tail-heavy markets

### DAG (Directed Acyclic Graph)

Located in `src/models/dag/`

**DAGStepModel** - Lattice-based pricing using a recombining tree structure where `up_factor * down_factor = 1`. Adjacent nodes at the same depth connect to common children, reducing computational complexity compared to full binary trees.

- Parameters: `u` (up factor), `depth` (tree depth)
- Suitable for path-dependent and American-style derivative pricing

### Binary Tree

Located in `src/models/bin_tree/`

**BTStepModel** - Binomial lattice model for path-dependent option pricing. Implementation is partial.

## Data Loaders and Feeders

The framework handles irregularly sampled financial data through a two-layer abstraction: loaders for file access and feeders for streaming data into simulations.

### The Problem: Irregular Time Sampling

Real market data arrives at irregular intervals. Bid/ask updates, trades, and price changes do not occur on fixed schedules. When backtesting strategies that involve multiple data streams (derivative prices and underlying prices), these streams have different timestamps that must be synchronized.

### Data Loaders

Located in `src/data_loaders/`

**LazyLoader** maps a directory structure of `root_dir/date/strike.csv` files to queryable data. Files are loaded lazily only when accessed.

```python
loader = LazyLoader(root_dir="data/derivatives")
loader.query(date="2024-01-15", strike=50)  # Returns DataFrame
loader.iterate()  # Generator yielding (date, strike, DataFrame) tuples
```

### Data Feeders

Located in `src/data_feeder/`

**SimDataFeeder** handles the core problem of irregular time sampling during simulation. It takes historical data with arbitrary timestamps and provides a streaming interface synchronized to a timer.

```python
# Historical data with irregular timestamps
history = {
    'time': [1000, 1045, 1200, 1205, 2100, ...],  # Irregular intervals
    'value': [{bid: 0.45, ask: 0.47}, ...]
}

# Create feeder synchronized to a timer
timer = DeltaTimer(delta=60)  # Fixed 60-second simulation cycles
feeder = SimDataFeeder(start, end, history, timer)

# During simulation, feeder.get() returns the most recent
# historical value before the current simulation time
```

The algorithm maintains deques of timestamps and values. On each `get()` call, it advances through the historical data until `next_time > current_sim_time`, then returns the last complete data point. This provides forward-fill interpolation across irregular samples.

### Linked Feeders

Located in `src/backtester/linked_feeders.py`

**FeederCreator** synchronizes multiple data feeders (derivative and underlying) to a shared timer. Both feeders consume data in lockstep at timer cycles, even though their underlying historical data has different timestamps.

```python
timer = DeltaTimer(60)
under_feeder = SimDataFeeder(start, end, underlying_data, timer)
deriv_feeder = SimDataFeeder(start, end, derivative_data, timer)

# Both feeders now return data aligned to the same time points
while not timer.is_finished():
    under_price = under_feeder.get()
    deriv_price = deriv_feeder.get()
    # Process synchronized data...
    timer.cycle()
```

This architecture enables:

- Backtesting with real market data that has irregular tick times
- Synchronizing multiple data streams with different sampling rates
- Memory-efficient streaming via deques and lazy file loading

## Project Structure

```
kalshi/
├── src/
│   ├── base/                    # Abstract base classes
│   │   ├── base_model.py        # Pricing model interface
│   │   ├── base_data_feeder.py  # Data stream interface
│   │   ├── base_data_loader.py  # File loading interface
│   │   ├── base_market.py       # Market/trading interface
│   │   ├── base_agent.py        # Strategy interface
│   │   └── base_timer.py        # Time simulation interface
│   │
│   ├── models/                  # Pricing models
│   │   ├── geom_bm/             # GBM step and range models
│   │   ├── geom_cauchy/         # Cauchy step and range models
│   │   ├── dag/                 # DAG lattice model
│   │   └── bin_tree/            # Binary tree model
│   │
│   ├── data_loaders/            # File access layer
│   │   └── lazy_loader.py
│   │
│   ├── data_feeder/             # Data streaming layer
│   │   ├── sim_data_feeder.py
│   │   └── connected_data_feeder.py
│   │
│   ├── agents/                  # Trading strategies
│   │   └── hedging_agent.py     # Delta hedge implementation
│   │
│   ├── markets/                 # Trading venues
│   │   └── sim_kalshi_market.py
│   │
│   ├── timers/                  # Time management
│   │   ├── accelerated_timer.py
│   │   ├── delta_timer.py
│   │   └── discrete_timer.py
│   │
│   ├── orders/                  # Order types
│   │   ├── limit_order.py
│   │   └── market_order.py
│   │
│   └── backtester/              # Simulation orchestration
│       └── linked_feeders.py
│
├── scripts/
│   └── gbm_backtest.py          # Parameter grid search
│
└── notebooks/                   # Analysis notebooks
```

## Model Comparison

| Model | Distribution | Value | IV | Delta | Gamma | Vega | Theta | Fat Tails |
|-------|-------------|----------------|-----|-------|-------|------|-------|-----------|
| GBMStep | Log-normal | Yes | Yes | Yes | Yes | Yes | Yes | No |
| GBMRange | Log-normal | Yes | Yes | Yes | Yes | Yes | Yes | No |
| CauchyStep | Cauchy | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| CauchyRange | Cauchy | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| DAGStep | Binomial | Yes | No | Yes | No | No | No | No |
| BTStep | Binomial | No | No | No | No | No | No | No |

## Dependencies

See `requirements.txt`: numpy, scipy, pandas, matplotlib, tqdm
