"""
Synthetic Data Generator for Adobe Structure Degradation Analysis
==================================================================

This script generates synthetic data that preserves the statistical properties
and correlations observed in real adobe structure degradation data, while
protecting the privacy and confidentiality of the actual Fort Union site data.

Educational Purpose:
-------------------
This synthetic dataset allows researchers and students to learn data-driven
preservation techniques without access to sensitive historical site data.

Author: Rebecca Napolitano, Penn State University
Grant: Data-Driven Heritage Preservation (NCPTT)
"""

import pandas as pd
import numpy as np
from scipy import stats

# Set random seed for reproducibility
np.random.seed(42)

def generate_synthetic_adobe_data(n_samples=67):
    """
    Generate synthetic adobe wall degradation data.
    
    Parameters:
    -----------
    n_samples : int
        Number of wall sections to simulate (default: 67, matching FOUN dataset)
    
    Returns:
    --------
    pd.DataFrame
        Synthetic dataset with degradation metrics
    """
    
    # Initialize data dictionary
    data = {}
    
    # Generate Wall IDs
    data['Wall ID'] = [f'Wall_{i:03d}' for i in range(1, n_samples + 1)]
    
    # --- GEOMETRIC FEATURES (Primary Drivers) ---
    # Wall Height: 1-5 scale (1=full height, 5=minimal remaining)
    # Distribution: Most walls partially degraded
    data['Height'] = np.random.choice([1, 2, 3, 4, 5], size=n_samples, p=[0.1, 0.25, 0.35, 0.2, 0.1])
    
    # Foundation Height: Exposed foundation in inches (0-48")
    # Higher values indicate more exposure (vulnerability driver)
    data['Foundation Height'] = np.random.gamma(shape=2, scale=6, size=n_samples).astype(int)
    data['Foundation Height'] = np.clip(data['Foundation Height'], 0, 48)
    
    # --- STRUCTURAL DEGRADATION (correlated with height) ---
    # Out of Plane: 0-5 scale (instability factor)
    # Correlation: Taller walls (lower Height value) have less out-of-plane
    out_of_plane_base = np.random.poisson(lam=2, size=n_samples)
    height_effect = (data['Height'] - 3) * 0.5  # Shorter walls lean more
    data['Out of Plane'] = np.clip(out_of_plane_base + height_effect, 0, 5).astype(int)
    
    # Structural Cracking: 0-5 scale
    # Correlated with Out of Plane and Foundation exposure
    cracking_base = np.random.poisson(lam=2, size=n_samples)
    data['Structural Cracking'] = np.clip(
        cracking_base + 0.3 * data['Out of Plane'] + 0.05 * data['Foundation Height'], 
        0, 5
    ).astype(int)
    
    # Cap Deterioration: 0-5 scale (highly correlated with total degradation)
    # More exposed = more cap damage
    cap_base = np.random.poisson(lam=2.5, size=n_samples)
    cap_height_effect = (5 - data['Height']) * 0.4
    data['Cap Deterioration'] = np.clip(cap_base + cap_height_effect, 0, 5).astype(int)
    
    # Cracking at Wall Junction: 0-5 scale
    data['Cracking Junction'] = np.random.poisson(lam=1.5, size=n_samples)
    data['Cracking Junction'] = np.clip(data['Cracking Junction'], 0, 5)
    
    # --- SILL FEATURES (Independent Factor 1) ---
    # Sills are architectural details with independent failure mechanism
    sill_degradation = np.random.poisson(lam=2, size=n_samples)
    noise = np.random.normal(0, 0.5, n_samples)
    
    data['Sill 1'] = np.clip(sill_degradation + noise, 0, 5).astype(int)
    data['Sill 2'] = np.clip(sill_degradation + noise * 0.8, 0, 5).astype(int)  # Highly correlated
    
    # --- SURFACE COAT FEATURES (Factor 2) ---
    # Coat Cracking and Loss (correlated with lintel deterioration)
    coat_base = np.random.poisson(lam=2, size=n_samples)
    
    data['Coat 1 Cracking'] = np.clip(coat_base + np.random.normal(0, 1, n_samples), 0, 5).astype(int)
    data['Coat 1 Loss'] = np.clip(coat_base * 0.6 + np.random.poisson(1, n_samples), 0, 5).astype(int)
    data['Coat 2 Cracking'] = np.clip(coat_base + np.random.normal(0, 1.2, n_samples), 0, 5).astype(int)
    data['Coat 2 Loss'] = np.clip(coat_base * 0.5 + np.random.poisson(1, n_samples), 0, 5).astype(int)
    
    # Lintel Deterioration (coupled with coat cracking)
    data['Lintel Deterioration'] = np.clip(
        0.6 * data['Coat 1 Cracking'] + np.random.poisson(1, n_samples), 
        0, 5
    ).astype(int)
    
    # --- SURFACE LOSS AT DIFFERENT LEVELS ---
    # More loss at top (exposed) and bottom (splash)
    data['Surface Loss Top'] = np.random.poisson(lam=2.5, size=n_samples)
    data['Surface Loss Top'] = np.clip(data['Surface Loss Top'], 0, 5)
    
    data['Surface Loss Mid'] = np.random.poisson(lam=1.5, size=n_samples)
    data['Surface Loss Mid'] = np.clip(data['Surface Loss Mid'], 0, 5)
    
    data['Surface Loss Low'] = np.random.poisson(lam=2, size=n_samples)
    data['Surface Loss Low'] = np.clip(data['Surface Loss Low'] + 0.05 * data['Foundation Height'], 0, 5).astype(int)
    
    # --- FOUNDATION FEATURES ---
    # Foundation Displacement: 0-5 scale
    foundation_effect = 0.08 * data['Foundation Height']
    data['Foundation Displacement 1'] = np.clip(
        np.random.poisson(1, n_samples) + foundation_effect, 0, 5
    ).astype(int)
    data['Foundation Displacement 2'] = np.clip(
        np.random.poisson(1, n_samples) + foundation_effect * 0.9, 0, 5
    ).astype(int)
    
    # Foundation Mortar Condition: 0-5 scale
    data['Foundation Mortar 1'] = np.random.poisson(lam=2, size=n_samples)
    data['Foundation Mortar 1'] = np.clip(data['Foundation Mortar 1'], 0, 5)
    data['Foundation Mortar 2'] = np.clip(data['Foundation Mortar 1'] + np.random.normal(0, 0.5, n_samples), 0, 5).astype(int)
    
    # Foundation Stone Deterioration
    data['Foundation Stone Det'] = np.clip(
        np.random.poisson(2, n_samples) + 0.05 * data['Foundation Height'], 0, 5
    ).astype(int)
    
    # --- TREATMENT HISTORY (Binary) ---
    # Treatment presence (slightly correlated with existing damage)
    treatment_prob = 0.3 + 0.01 * (data['Structural Cracking'] + data['Out of Plane'])
    data['Treatment'] = (np.random.random(n_samples) < treatment_prob).astype(int)
    
    # Bracing presence (on more damaged walls)
    bracing_prob = 0.2 + 0.05 * (data['Out of Plane'] + data['Structural Cracking'])
    data['Bracing'] = (np.random.random(n_samples) < bracing_prob).astype(int)
    
    # Bracing Score (condition of bracing, if present)
    data['Bracing Score'] = np.where(
        data['Bracing'] == 1,
        np.random.choice([1, 2, 3, 4, 5], n_samples, p=[0.1, 0.2, 0.3, 0.25, 0.15]),
        0
    )
    
    # --- OTHER FEATURES ---
    # Animal Activity
    data['Animal Activity'] = np.random.poisson(lam=0.5, size=n_samples)
    data['Animal Activity'] = np.clip(data['Animal Activity'], 0, 3)
    
    # Fireplace proximity (categorical)
    data['Fireplace'] = np.random.choice([0, 1, 2], size=n_samples, p=[0.7, 0.2, 0.1])
    
    # Point Cloud Metrics (geometric measurements from LiDAR)
    data['Point Cloud Mean'] = np.random.normal(0, 2.5, n_samples)
    data['Point Cloud Deviation'] = np.abs(np.random.exponential(1.5, n_samples))
    
    # --- CALCULATE TOTAL DEGRADATION SCORE ---
    # This is the TARGET variable for ML models
    # Weighted combination of key metrics
    total_score = (
        data['Cap Deterioration'] * 3.0 +
        data['Out of Plane'] * 2.8 +
        data['Height'] * 2.5 +
        data['Structural Cracking'] * 2.5 +
        data['Coat 1 Cracking'] * 1.5 +
        data['Coat 2 Cracking'] * 1.5 +
        data['Sill 1'] * 1.2 +
        data['Sill 2'] * 1.2 +
        data['Lintel Deterioration'] * 1.8 +
        data['Surface Loss Top'] * 1.0 +
        data['Surface Loss Mid'] * 0.8 +
        data['Surface Loss Low'] * 1.0 +
        data['Foundation Height'] * 0.15 +
        data['Foundation Stone Det'] * 1.5 +
        data['Bracing'] * 1.5  # Reflects reactive installation
    )
    
    # Add some noise and normalize
    total_score = total_score + np.random.normal(0, 2, n_samples)
    data['Total Scr'] = np.clip(total_score, 0, 100)
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    return df


def save_synthetic_data(df, filename='synthetic_adobe_data.csv'):
    """Save synthetic data to CSV with metadata."""
    df.to_csv(filename, index=False)
    print(f"Synthetic data saved to {filename}")
    print(f"Shape: {df.shape}")
    print(f"\nFirst few rows:")
    print(df.head())
    print(f"\nBasic statistics:")
    print(df.describe())


if __name__ == "__main__":
    # Generate synthetic dataset
    synthetic_df = generate_synthetic_adobe_data(n_samples=67)
    
    # Save to file
    save_synthetic_data(synthetic_df, 'synthetic_adobe_data.csv')
    
    # Verify key correlations are preserved
    print("\n" + "="*50)
    print("VALIDATION: Key Correlations")
    print("="*50)
    print(f"Total Scr vs Cap Deterioration: {synthetic_df['Total Scr'].corr(synthetic_df['Cap Deterioration']):.3f}")
    print(f"Total Scr vs Out of Plane: {synthetic_df['Total Scr'].corr(synthetic_df['Out of Plane']):.3f}")
    print(f"Total Scr vs Height: {synthetic_df['Total Scr'].corr(synthetic_df['Height']):.3f}")
    print(f"Total Scr vs Structural Cracking: {synthetic_df['Total Scr'].corr(synthetic_df['Structural Cracking']):.3f}")
    print(f"Sill 1 vs Sill 2: {synthetic_df['Sill 1'].corr(synthetic_df['Sill 2']):.3f}")
    print(f"Coat 1 Cracking vs Lintel Det: {synthetic_df['Coat 1 Cracking'].corr(synthetic_df['Lintel Deterioration']):.3f}")
