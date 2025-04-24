#!/usr/bin/env python3

import numpy as np
import pandas as pd
import argparse
import json
from collections import OrderedDict

def parse_arguments():
    parser = argparse.ArgumentParser(description='Calculate bootstrap confidence intervals for sequence identity data.')
    parser.add_argument('input_file', help='Path to the input data file (tab-delimited)')
    parser.add_argument('-o', '--output', default='bootstrap_results.json', 
                       help='Output JSON file path (default: bootstrap_results.json)')
    parser.add_argument('-n', '--n_bootstrap', type=int, default=10000,
                       help='Number of bootstrap iterations (default: 10000)')
    parser.add_argument('-c', '--confidence', type=float, default=95,
                       help='Confidence interval percentage (default: 95)')
    parser.add_argument('-s', '--seed', type=int, default=42,
                       help='Random seed for reproducibility (default: 42)')
    return parser.parse_args()

def bootstrap_ci(data, n_bootstrap=10000, sample_size=None, ci=95, seed=42):
    """
    Calculate bootstrap confidence intervals for data.
    
    Args:
        data: Input data array
        n_bootstrap: Number of bootstrap iterations
        sample_size: Sample size for each iteration (None for same as input)
        ci: Confidence interval percentage
        seed: Random seed
        
    Returns:
        Tuple of (original mean, CI lower bound, CI upper bound)
    """
    np.random.seed(seed)
    sample_size = sample_size if sample_size else len(data)
    boot_means = np.empty(n_bootstrap)
    
    for i in range(n_bootstrap):
        sample = np.random.choice(data, size=sample_size, replace=True)
        boot_means[i] = np.mean(sample)
    
    ci_low = np.percentile(boot_means, (100 - ci) / 2)
    ci_high = np.percentile(boot_means, 100 - (100 - ci) / 2)
    return np.mean(data), ci_low, ci_high

def main():
    args = parse_arguments()
    
    # Read input data
    try:
        data = pd.read_csv(args.input_file, sep="\t")
    except Exception as e:
        print(f"Error reading input file: {str(e)}")
        return

    # Process each column (skip first column assumed to be index)
    columns_to_analyze = data.columns[1:]
    results = OrderedDict()
    
    print(f"\nAnalyzing {len(columns_to_analyze)} columns with {args.n_bootstrap} bootstrap iterations...\n")
    
    for column in columns_to_analyze:
        column_data = data[column].dropna().values
        if len(column_data) > 0:
            original_mean, ci_lower, ci_upper = bootstrap_ci(
                column_data,
                n_bootstrap=args.n_bootstrap,
                sample_size=len(column_data),
                ci=args.confidence,
                seed=args.seed
            )
            results[column] = {
                "mean": original_mean,
                "ci_lower": ci_lower,
                "ci_upper": ci_upper,
                "n_samples": len(column_data)
            }
            print(f"{column:>15}: {original_mean:.4f} [{ci_lower:.4f}, {ci_upper:.4f}] (n={len(column_data)})")
        else:
            print(f"{column:>15}: No valid data - skipped")

    # Save results
    try:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=4)
        print(f"\nResults saved to {args.output}")
    except Exception as e:
        print(f"Error saving results: {str(e)}")

if __name__ == '__main__':
    main()