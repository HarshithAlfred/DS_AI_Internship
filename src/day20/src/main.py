import argparse
import os
import sys

# Add src to path if needed (though running as module is better)
sys.path.append(os.path.join(os.path.dirname(__file__)))

from generator import CustomerDataGenerator
from reporter import DataReporter

def main():
    parser = argparse.ArgumentParser(description="Professional Customer Analytics Dataset Generator")
    
    parser.add_argument("--rows", type=int, default=250, help="Number of base rows to generate (default: 250)")
    parser.add_argument("--output", type=str, default="data/customer_analytics.csv", help="Output path for CSV (default: data/customer_analytics.csv)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility (default: 42)")
    parser.add_argument("--report", action="store_true", help="Generate a summary report after data generation")
    parser.add_argument("--report-path", type=str, default="reports/data_summary.txt", help="Output path for the report (default: reports/data_summary.txt)")

    args = parser.parse_args()

    # Ensure directories exist
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    if args.report:
        os.makedirs(os.path.dirname(args.report_path) or ".", exist_ok=True)

    print(f"Initializing Generator with seed: {args.seed}")
    gen = CustomerDataGenerator(seed=args.seed)
    
    print(f"Generating {args.rows} customer records...")
    df = gen.generate(n_rows=args.rows, output_path=args.output)
    
    print(f"Dataset saved to: {args.output}")
    print(f"Total entries (including duplicates): {len(df)}")

    if args.report:
        print("Generating dataset report...")
        DataReporter.generate_report(df, output_path=args.report_path)
    
    print("\nProcess completed successfully!")

if __name__ == "__main__":
    main()
