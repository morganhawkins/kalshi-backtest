from warnings import warn

import numpy as np
from scipy.special import erf as erf
from scipy.special import erfinv as erfinv

def value(u_price: float, strike: int, sigma: float, mu: float, tte: float) -> float:
    """_summary_

    Args:
        price (float): price of contract
        u_price (float): price of underlying asset
        strike (int): strike price of contract
        sigma (float): volatility in standard dev of hourly log(return)
        mu (float): expected return in expected hourly return
        tte (float): time to contract expiration in hours

    Returns:
        float: value of derivative under assumtions of Black-Scholes
    """
            
    if tte <= 0: 
        return int(u_price >= strike) #if there is 0 time to expiry, return the expiration value

    deviations_to_strike = ( np.log(strike) - np.log(u_price) - (tte*mu) ) / ( np.sqrt(2*tte) * sigma )
    deriv_price = .5 * (1 - erf(deviations_to_strike))
    return deriv_price

def iv(price: float, u_price: float, strike: int, mu: float, tte: float) -> float:
    """_summary_

    Args:
        price (float): price of contract
        u_price (float): price of underlying asset
        strike (int): strike price of contract
        sigma (float): volatility in standard dev of hourly log(return)
        mu (float): expected return in expected hourly return
        tte (float): time to contract expiration in hours

    Raises:
        ValueError: tte is less than 0

    Returns:
        float: implied volatility of the underlying asset
    """
    if tte<=0:
        raise ValueError("Time to expiration must be strictly positive")
    
    if price == .5:
        warn("IV not defined for step contracts with market price of .5") 
        return np.nan
    
    numerator = np.log(strike) - np.log(u_price) - (tte*mu)
    denominator = np.sqrt(2*tte) * erfinv(1- (2*price))

    implied_vol = numerator/denominator 

    if implied_vol >= 0:
        return implied_vol
    else:
        # warn_string = f"Negative IV result, implied future expected return in underlying asset {u_price} {strike} {price}"
        # warn(warn_string)
        return np.nan 

def delta(u_price: float, strike: int, sigma: float, mu: float, tte: float) -> float:
    """_summary_

    Args:
        price (float): price of contract
        u_price (float): price of underlying asset
        strike (int): strike price of contract
        sigma (float): volatility in standard dev of hourly log(return)
        mu (float): expected return in expected hourly return
        tte (float): time to contract expiration in hours

    Returns:
        float: sesitivity to price of underlying
    """
    deviations_to_strike = ( np.log(strike) - np.log(u_price) - (tte*mu) ) / ( np.sqrt(2*tte) * sigma )
    denominator = u_price * sigma * np.sqrt(2 * tte * np.pi)
    return np.exp(-(deviations_to_strike**2)) / denominator

def vega(u_price: float, strike: int, sigma: float, mu: float, tte: float) -> float:
    """_summary_

    Args:
        price (float): price of contract
        u_price (float): price of underlying asset
        strike (int): strike price of contract
        sigma (float): volatility in standard dev of hourly log(return)
        mu (float): expected return in expected hourly return
        tte (float): time to contract expiration in hours

    Returns:
        float: sensitivity to underlying security volatility
    """
    expected_units_to_strike = np.log(strike) - np.log(u_price) - (tte*mu)
    formula_lhs = np.exp(-(expected_units_to_strike)**2 / (2 * tte * (sigma**2)))
    return formula_lhs * ( (expected_units_to_strike) / (sigma**2 * np.sqrt(2 * tte * np.pi)))

def theta(u_price: float, strike: int, sigma: float, mu: float, tte: float) -> float:
    """_summary_

    Args:
        price (float): price of contract
        u_price (float): price of underlying asset
        strike (int): strike price of contract
        sigma (float): volatility in standard dev of hourly log(return)
        mu (float): expected return in expected hourly return
        tte (float): time to contract expiration in hours

    Returns:
        float: sensitiviy to time to expiration
    """
    formula_lhs = (np.log(u_price) - np.log(strike) - (tte*mu)) / (sigma*np.sqrt(8 * np.pi * (tte**3)))
    return formula_lhs * np.exp(-(np.log(strike) - np.log(u_price) - (tte*mu) )**2 / (2 * tte * (sigma**2)))

def gamma(u_price: float, strike: int, sigma: float, mu: float, tte: float) -> float:
    """_summary_

    Args:
        price (float): price of contract
        u_price (float): price of underlying asset
        strike (int): strike price of contract
        sigma (float): volatility in standard dev of hourly log(return)
        mu (float): expected return in expected hourly return
        tte (float): time to contract expiration in hours

    Returns:
        float: delta's sensitivity to changes in underlying'sprice
    """
    formula_lhs = np.exp(-(np.log(strike) - np.log(u_price) - (tte*mu) )**2 / (2 * tte * (sigma**2)))
    return formula_lhs * ( (np.log(strike) - np.log(u_price) - (tte*(sigma**2 + mu))) / ( tte * (sigma**3) * (u_price**2) * np.sqrt(2 * tte * np.pi)) )




