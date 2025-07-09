
import numpy as np
import pandas as pd
from scipy.optimize import minimize
def get_portfolio(risk_tolerance):
    
    # Test Dokimes gia to get_portfolio
    
    if not 0 <= risk_tolerance <= 1:
        raise ValueError("Risk tolerance must be between 0 and 1.")

    
    assets = [
        {'name': 'US Stocks (VTI)', 'return': 0.085, 'risk': 0.18, 'type': 'equity'},
        {'name': 'Gold (GLD)', 'return': 0.045, 'risk': 0.15, 'type': 'commodity'},
        {'name': 'Real Estate (VNQ)', 'return': 0.065, 'risk': 0.17, 'type': 'real_estate'},
        {'name': 'Corporate Bonds (LQD)', 'return': 0.048, 'risk': 0.10, 'type': 'bond'},
        {'name': 'Treasuries (TLT)', 'return': 0.038, 'risk': 0.12, 'type': 'bond'},
        {'name': 'Cryptocurrency (BTC-USD)', 'return': 0.22, 'risk': 0.40, 'type': 'crypto'},
        {'name': 'Emerging Markets (VWO)', 'return': 0.11, 'risk': 0.24, 'type': 'equity'},
        {'name': 'Small Cap Value (IWN)', 'return': 0.095, 'risk': 0.22, 'type': 'equity'},
        {'name': 'Cash Equivalents', 'return': 0.028, 'risk': 0.01, 'type': 'cash'}
    ]
    
    
    if risk_tolerance < 0.3:
        assets = [a for a in assets if a['type'] not in ['crypto', 'small_cap']]
    elif risk_tolerance < 0.6:
        assets = [a for a in assets if a['type'] != 'crypto']
    
    asset_names = [a['name'] for a in assets]
    mean_returns = np.array([a['return'] for a in assets])
    risks = np.array([a['risk'] for a in assets])
    
    # Improved dynamic correlation matrix
    corr_matrix = np.eye(len(assets))
    for i in range(len(assets)):
        for j in range(i+1, len(assets)):
            # Base correlation based on asset types
            if assets[i]['type'] == assets[j]['type']:
                corr = 0.6 - (0.2 * risk_tolerance)  # More diversification for higher risk
            else:
                # Negative correlations for bonds vs equities at higher risk levels
                if ('bond' in [assets[i]['type'], assets[j]['type']] and 
                    'equity' in [assets[i]['type'], assets[j]['type']]):
                    corr = -0.1 * risk_tolerance
                else:
                    corr = 0.3 - (0.2 * risk_tolerance)
            corr_matrix[i,j] = corr_matrix[j,i] = max(min(corr, 0.9), -0.5)
    
    cov_matrix = np.outer(risks, risks) * corr_matrix
    
    # Portfolio metrics
    def portfolio_return(weights):
        return np.dot(weights, mean_returns)
    
    def portfolio_volatility(weights):
        return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    
    def sharpe_ratio(weights):
        vol = portfolio_volatility(weights)
        return (portfolio_return(weights)) / (vol + 1e-9)
    
    # Enhanced objective function - more aggressive Sharpe maximization
    def objective(weights):
        base_sharpe = sharpe_ratio(weights)
        # Penalize concentration and reward diversification
        diversification_bonus = 0.5 * np.sqrt(np.sum(weights**2)) / len(weights)
        # More aggressive optimization for higher risk tolerance
        return -(base_sharpe * (1 + risk_tolerance) + diversification_bonus)
    
    # Dynamic volatility targeting - wide range (4% to 35%)
    target_volatility = 0.04 + (risk_tolerance * 0.31)
    
    constraints = [
        {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
        {'type': 'ineq', 'fun': lambda x: target_volatility - portfolio_volatility(x)}
    ]
    
    
    bounds = []
    for asset in assets:
        asset_type = asset['type']
        
        if asset_type == 'cash':
            max_bound = max(0.1, 0.3 - (risk_tolerance * 0.25))
            bounds.append((0.0, max_bound))
        elif asset_type == 'bond':
            max_bound = 0.4 - (risk_tolerance * 0.3)
            bounds.append((0.05, max_bound))
        elif asset_type == 'crypto':
            min_bound = 0.0 if risk_tolerance < 0.7 else 0.05
            max_bound = min(0.25, 0.05 + ((risk_tolerance-0.7)*0.5))
            bounds.append((min_bound, max_bound))
        elif asset_type == 'equity':
            min_bound = 0.1 if risk_tolerance > 0.4 else 0.05
            max_bound = min(0.5, 0.3 + (risk_tolerance*0.4))
            bounds.append((min_bound, max_bound))
        else:
            bounds.append((0.0, 0.4))
    
    
    initial_guess = np.zeros(len(assets))
    for i, asset in enumerate(assets):
        if asset['type'] == 'cash':
            initial_guess[i] = 0.2 - (risk_tolerance * 0.15)
        elif asset['type'] == 'bond':
            initial_guess[i] = 0.3 - (risk_tolerance * 0.2)
        elif asset['type'] == 'equity':
            initial_guess[i] = 0.2 + (risk_tolerance * 0.3)
        else:
            initial_guess[i] = 0.1
    initial_guess /= initial_guess.sum()
    
    
    result = minimize(
        objective,
        initial_guess,
        method='SLSQP',
        bounds=bounds,
        constraints=constraints,
        options={'maxiter': 2000, 'ftol': 1e-10}
    )
    
    weights = result.x if result.success else initial_guess
    weights = np.maximum(weights, 0)
    weights /= weights.sum()
    
    # Filter small allocations (<1%) and renormalize
    valid_indices = [i for i, w in enumerate(weights) if w >= 0.01]
    filtered_weights = weights[valid_indices]
    filtered_weights /= filtered_weights.sum()
    filtered_assets = [asset_names[i] for i in valid_indices]
    
    # Calculate metrics
    final_return = np.dot(filtered_weights, mean_returns[valid_indices])
    final_volatility = np.sqrt(np.dot(filtered_weights.T, 
                                   np.dot(cov_matrix[np.ix_(valid_indices, valid_indices)], 
                                          filtered_weights)))
    final_sharpe = (final_return ) / (final_volatility + 1e-9)
    
    allocations = {
        asset: round(w * 100, 1)
        for asset, w in zip(filtered_assets, filtered_weights)
    }
    
    return {
        'allocations': allocations,
        'metrics': {
            'expected_return': round(final_return * 100, 2),
            'expected_volatility': round(final_volatility * 100, 2),
            'sharpe_ratio': round(final_sharpe, 2),
            'diversification': len(allocations),
            'risk_category': (
                'Very Conservative' if risk_tolerance < 0.2 else
                'Conservative' if risk_tolerance < 0.4 else
                'Moderate' if risk_tolerance < 0.6 else
                'Aggressive' if risk_tolerance < 0.8 else
                'Very Aggressive'
            )
        }
    }
risk_tolerance = 0.3
portfolio = get_portfolio(risk_tolerance)


print("Portfolio Allocations:")
for asset, allocation in portfolio['allocations'].items():
    print(f"{asset}: {allocation}%")

print("\nPortfolio Metrics:")
for metric, value in portfolio['metrics'].items():
    print(f"{metric}: {value}")