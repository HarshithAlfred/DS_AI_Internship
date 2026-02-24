import pandas as pd
import numpy as np
import random
from typing import Optional, List

class CustomerDataGenerator:
    """
    A professional class for generating synthetic customer analytics data.
    """
    def __init__(self, seed: int = 42):
        self.seed = seed
        self.reset_seed()
        
        self.cities = ["Bangalore", "Mumbai", "Delhi", "Chennai", "Hyderabad", "Pune"]
        self.education_levels = ["Bachelors", "Masters", "PhD"]
        self.marital_statuses = ["Single", "Married"]
        self.devices = ["Mobile", "Laptop", "Tablet", "Desktop"]
        self.genders = ["Male", "Female"]
        self.columns = [
            "CustomerID", "Age", "Gender", "City", "Education", "MaritalStatus",
            "AnnualIncome", "SpendingScore", "YearsEmployed", "PurchaseFrequency",
            "OnlineVisitsPerMonth", "ReturnedItems", "PreferredDevice", "LastPurchaseAmount"
        ]

    def reset_seed(self):
        np.random.seed(self.seed)
        random.seed(self.seed)

    def generate_base_data(self, n_rows: int) -> pd.DataFrame:
        """Generates the initial clean rows of data."""
        rows = []
        for customer_id in range(1001, 1001 + n_rows):
            age = np.random.randint(21, 55)
            experience = max(1, age - np.random.randint(20, 28))
            
            # Annual Income (Normal Distribution)
            income = np.random.normal(70000, 20000)
            
            # Inject OUTLIERS (High earners)
            if random.random() < 0.02:
                income = np.random.randint(200000, 500000)
            income = int(abs(income))

            # Spending Score (Correlated with Income)
            spending_score = np.clip(
                np.random.normal(60 - (income / 5000), 15),
                5, 95
            )

            rows.append([
                customer_id,
                age,
                random.choice(self.genders),
                random.choice(self.cities),
                random.choice(self.education_levels),
                random.choice(self.marital_statuses),
                income,
                int(spending_score),
                experience,
                np.random.randint(1, 25),
                np.random.randint(3, 30),
                np.random.randint(0, 5),
                random.choice(self.devices),
                np.random.randint(500, 5000)
            ])
        
        return pd.DataFrame(rows, columns=self.columns)

    def inject_noise(self, df: pd.DataFrame, missing_frac: float = 0.05, n_duplicates: int = 5) -> pd.DataFrame:
        """Injects missing values and duplicates into the dataframe."""
        # Missing values
        for col in ["Education", "AnnualIncome"]:
            df.loc[df.sample(frac=missing_frac).index, col] = None
        
        # Duplicates
        duplicates = df.sample(n_duplicates)
        df = pd.concat([df, duplicates], ignore_index=True)
        
        return df

    def generate(self, n_rows: int = 250, output_path: str = "data/customer_analytics.csv") -> pd.DataFrame:
        """Main method to generate and save the dataset."""
        df = self.generate_base_data(n_rows)
        df = self.inject_noise(df)
        df.to_csv(output_path, index=False)
        return df
