from warnings import warn

import numpy as np


def value(u_price: float, strike: int, scale: float, loc: float, tte: float) -> float:
    """Calculate the value of a step contract under Cauchy log returns.

    Args:
        u_price (float): price of underlying asset
        strike (int): strike price of contract
        scale (float): scale parameter of hourly log returns (Cauchy)
        loc (float): location parameter of hourly log returns (Cauchy)
        tte (float): time to contract expiration in hours

    Returns:
        float: probability that underlying >= strike at expiration
    """
    if tte <= 0:
        return int(u_price >= strike)

    # For Cauchy: P(X >= k) = 0.5 - (1/pi) * arctan((k - loc) / scale)
    # Here X = log(S_T/S_0) ~ Cauchy(tte*loc, tte*scale)
    # We want P(S_T >= K) = P(log(S_T) >= log(K)) = P(X >= log(K) - log(S_0))
    z = (np.log(strike) - np.log(u_price) - tte * loc) / (tte * scale)
    deriv_price = 0.5 - (1 / np.pi) * np.arctan(z)
    return deriv_price


def iv(price: float, u_price: float, strike: int, loc: float, tte: float) -> float:
    """Calculate implied scale (volatility analog) for Cauchy log returns.

    Args:
        price (float): price of contract
        u_price (float): price of underlying asset
        strike (int): strike price of contract
        loc (float): location parameter of hourly log returns (Cauchy)
        tte (float): time to contract expiration in hours

    Returns:
        float: implied scale parameter
    """
    if tte <= 0:
        raise ValueError("Time to expiration must be strictly positive")

    if price == 0.5:
        warn("IV not defined for step contracts with market price of .5")
        return np.nan

    # From value formula: price = 0.5 - (1/pi) * arctan(z)
    # Solving for scale:
    # arctan(z) = pi * (0.5 - price)
    # z = tan(pi * (0.5 - price))
    # (log(strike) - log(u_price) - tte*loc) / (tte*scale) = tan(pi * (0.5 - price))
    # scale = (log(strike) - log(u_price) - tte*loc) / (tte * tan(pi * (0.5 - price)))

    tan_val = np.tan(np.pi * (0.5 - price))

    if tan_val == 0:
        warn("IV undefined when tan(pi * (0.5 - price)) = 0")
        return np.nan

    numerator = np.log(strike) - np.log(u_price) - tte * loc
    implied_scale = numerator / (tte * tan_val)

    if implied_scale >= 0:
        return implied_scale
    else:
        return np.nan


def delta(u_price: float, strike: int, scale: float, loc: float, tte: float) -> float:
    """Calculate delta (sensitivity to underlying price) for Cauchy log returns.

    Args:
        u_price (float): price of underlying asset
        strike (int): strike price of contract
        scale (float): scale parameter of hourly log returns (Cauchy)
        loc (float): location parameter of hourly log returns (Cauchy)
        tte (float): time to contract expiration in hours

    Returns:
        float: sensitivity to price of underlying
    """
    # value = 0.5 - (1/pi) * arctan(z), where z = (log(strike) - log(u_price) - tte*loc) / (tte*scale)
    # d(value)/d(u_price) = -(1/pi) * 1/(1+z^2) * dz/d(u_price)
    # dz/d(u_price) = -1/(u_price * tte * scale)
    # delta = (1/pi) * 1/(1+z^2) * 1/(u_price * tte * scale)

    z = (np.log(strike) - np.log(u_price) - tte * loc) / (tte * scale)
    return 1 / (np.pi * u_price * tte * scale * (1 + z**2))


def vega(u_price: float, strike: int, scale: float, loc: float, tte: float) -> float:
    """Calculate vega (sensitivity to scale parameter) for Cauchy log returns.

    Args:
        u_price (float): price of underlying asset
        strike (int): strike price of contract
        scale (float): scale parameter of hourly log returns (Cauchy)
        loc (float): location parameter of hourly log returns (Cauchy)
        tte (float): time to contract expiration in hours

    Returns:
        float: sensitivity to scale parameter
    """
    # value = 0.5 - (1/pi) * arctan(z)
    # dz/d(scale) = -(log(strike) - log(u_price) - tte*loc) / (tte * scale^2) = -z/scale
    # vega = -(1/pi) * 1/(1+z^2) * (-z/scale) = z / (pi * scale * (1+z^2))

    z = (np.log(strike) - np.log(u_price) - tte * loc) / (tte * scale)
    return z / (np.pi * scale * (1 + z**2))


def theta(u_price: float, strike: int, scale: float, loc: float, tte: float) -> float:
    """Calculate theta (sensitivity to time) for Cauchy log returns.

    Args:
        u_price (float): price of underlying asset
        strike (int): strike price of contract
        scale (float): scale parameter of hourly log returns (Cauchy)
        loc (float): location parameter of hourly log returns (Cauchy)
        tte (float): time to contract expiration in hours

    Returns:
        float: sensitivity to time to expiration
    """
    # z = (log(strike) - log(u_price) - tte*loc) / (tte*scale)
    # Let num = log(strike) - log(u_price) - tte*loc, den = tte*scale
    # dz/dtte = (d(num)/dtte * den - num * d(den)/dtte) / den^2
    #         = (-loc * tte*scale - (log(strike) - log(u_price) - tte*loc) * scale) / (tte*scale)^2
    #         = (-loc * tte - log(strike) + log(u_price) + tte*loc) / (tte^2 * scale)
    #         = (log(u_price) - log(strike)) / (tte^2 * scale)
    # theta = -(1/pi) * 1/(1+z^2) * dz/dtte
    #       = -(1/pi) * (log(u_price) - log(strike)) / (tte^2 * scale * (1+z^2))

    z = (np.log(strike) - np.log(u_price) - tte * loc) / (tte * scale)
    log_ratio = np.log(u_price) - np.log(strike)
    return -log_ratio / (np.pi * tte**2 * scale * (1 + z**2))


def gamma(u_price: float, strike: int, scale: float, loc: float, tte: float) -> float:
    """Calculate gamma (delta's sensitivity to underlying price) for Cauchy log returns.

    Args:
        u_price (float): price of underlying asset
        strike (int): strike price of contract
        scale (float): scale parameter of hourly log returns (Cauchy)
        loc (float): location parameter of hourly log returns (Cauchy)
        tte (float): time to contract expiration in hours

    Returns:
        float: delta's sensitivity to changes in underlying price
    """
    # delta = 1 / (pi * u_price * tte * scale * (1+z^2))
    # Let A = pi * tte * scale
    # delta = 1 / (A * u_price * (1+z^2))
    # d(delta)/d(u_price) = d/d(u_price) [1 / (A * u_price * (1+z^2))]
    #
    # Using quotient rule:
    # Let f = 1, g = A * u_price * (1+z^2)
    # d(delta)/d(u_price) = -1/g^2 * dg/d(u_price)
    # dg/d(u_price) = A * [(1+z^2) + u_price * 2z * dz/d(u_price)]
    # dz/d(u_price) = -1/(u_price * tte * scale)
    # dg/d(u_price) = A * [(1+z^2) - 2z/(tte * scale)]
    #
    # gamma = -A * [(1+z^2) - 2z/(tte*scale)] / (A * u_price * (1+z^2))^2
    #       = -[(1+z^2) - 2z/(tte*scale)] / (A * u_price^2 * (1+z^2)^2)

    z = (np.log(strike) - np.log(u_price) - tte * loc) / (tte * scale)
    A = np.pi * tte * scale
    numerator = (1 + z**2) - 2 * z / (tte * scale)
    denominator = A * u_price**2 * (1 + z**2)**2
    return -numerator / denominator
