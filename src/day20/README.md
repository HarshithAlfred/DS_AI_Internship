# Customer Analytics Dataset Generator

A professional synthetic data generator designed for EDA (Exploratory Data Analysis) practice. It generates realistic, messy datasets with missing values, outliers, and duplicates.

## Features
- **Class-Based Generator**: Modular and extensible data generation logic.
- **Noise Injection**: Automatically adds missing values, outliers, and duplicates to simulate real-world data.
- **CLI Support**: Easy to use command-line interface with configurable options.
- **Automated Reporting**: Generates a summary report of the dataset characteristics.

## Project Structure
```text
.
├── data/               # Generated CSV files
├── reports/            # Generated analysis reports
├── src/                # Source code
│   ├── generator.py    # Data generation logic
│   ├── reporter.py     # Simple EDA report generator
│   └── main.py         # CLI entry point
├── requirements.txt    # Dependencies
└── README.md           # This file
```

## Installation
```bash
pip install -r requirements.txt
```

## Usage
Run the script using the following command:

```bash
python src/main.py --rows 500 --report
```

### CLI Arguments
| Argument | Description | Default |
| :--- | :--- | :--- |
| `--rows` | Number of base rows to generate | 250 |
| `--output` | Path to save the generated CSV | data/customer_analytics.csv |
| `--seed` | Random seed for reproducibility | 42 |
| `--report` | Flag to generate a summary report | False |
| `--report-path` | Path to save the summary report | reports/data_summary.txt |

## Example Output
```text
Initializing Generator with seed: 42
Generating 500 customer records...
Dataset saved to: data/customer_analytics.csv
Total entries (including duplicates): 505
Generating dataset report...
Report generated at: reports/data_summary.txt

Process completed successfully!
```
