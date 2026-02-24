import pandas as pd
import os

class DataReporter:
    """
    Generates a simple summary report for a given dataset.
    """
    @staticmethod
    def generate_report(df: pd.DataFrame, output_path: str = "reports/data_summary.txt"):
        """Creates a text-based summary of the dataframe."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, "w") as f:
            f.write("===============================================================\n")
            f.write("DATASET CHARACTERISTICS REPORT\n")
            f.write("===============================================================\n\n")
            
            f.write(f"Total Rows: {df.shape[0]}\n")
            f.write(f"Total Columns: {df.shape[1]}\n\n")
            
            f.write("Column Types & Missing Values:\n")
            f.write("-" * 30 + "\n")
            null_counts = df.isnull().sum()
            for col in df.columns:
                null_pct = (null_counts[col] / len(df)) * 100
                f.write(f"{col:<20} | {str(df[col].dtype):<10} | Missing: {null_counts[col]} ({null_pct:.1f}%)\n")
            
            f.write("\nBasic Statistics for Numerical Columns:\n")
            f.write("-" * 30 + "\n")
            stats = df.describe().transpose()
            f.write(stats.to_string())
            
            f.write("\n\nDuplicate Rows Check:\n")
            f.write("-" * 30 + "\n")
            duplicates = df.duplicated().sum()
            f.write(f"Number of duplicate rows found: {duplicates}\n")
            
            f.write("\n===============================================================\n")
            f.write("Report generated successfully.\n")
            f.write("===============================================================\n")
        
        print(f"Report generated at: {output_path}")
