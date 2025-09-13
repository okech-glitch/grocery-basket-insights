import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker for realistic data
fake = Faker()
np.random.seed(42)  # For reproducibility

# Define product catalog
products = [
    {"product_id": 101, "product_name": "Diapers", "category": "Baby Products", "price": 15.99},
    {"product_id": 102, "product_name": "Baby Food", "category": "Baby Products", "price": 3.99},
    {"product_id": 103, "product_name": "Milk", "category": "Dairy", "price": 2.99},
    {"product_id": 104, "product_name": "Bread", "category": "Bakery", "price": 1.99},
    {"product_id": 105, "product_name": "Butter", "category": "Dairy", "price": 4.49},
    {"product_id": 106, "product_name": "Cereal", "category": "Breakfast", "price": 3.49},
    {"product_id": 107, "product_name": "Eggs", "category": "Dairy", "price": 2.79},
    {"product_id": 108, "product_name": "Coffee", "category": "Beverages", "price": 6.99},
    {"product_id": 109, "product_name": "Pasta", "category": "Pantry", "price": 1.49},
    {"product_id": 110, "product_name": "Sauce", "category": "Pantry", "price": 2.29},
]

# Define stores
stores = [55, 56, 57, 58]

# Generate transactions
def generate_transactions(num_transactions, is_train=True):
    data = []
    transaction_id = 1
    customer_id = 1000

    for _ in range(num_transactions):
        # Random basket size (2-10 items)
        basket_size = random.randint(2, 10)
        # Randomly select products for the basket
        basket_products = random.sample(products, basket_size)
        purchase_date = fake.date_between(start_date="-1y", end_date="today")
        
        # Assign bundle target based on rules (e.g., Diapers + Baby Food)
        for product in basket_products:
            row = {
                "transaction_id": transaction_id,
                "customer_id": customer_id,
                "product_id": product["product_id"],
                "product_name": product["product_name"],
                "product_category": product["category"],
                "quantity": random.randint(1, 5),
                "price": product["price"],
                "purchase_date": purchase_date.strftime("%Y-%m-%d"),
                "store_id": random.choice(stores),
            }
            # Bundle logic: Diapers (101) and Baby Food (102) often bought together
            if is_train:
                is_bundle = 1 if (
                    (product["product_id"] == 101 and any(p["product_id"] == 102 for p in basket_products)) or
                    (product["product_id"] == 102 and any(p["product_id"] == 101 for p in basket_products)) or
                    random.random() < 0.3  # 30% chance for other products
                ) else 0
                row["is_bundle_target"] = is_bundle
            data.append(row)
        
        transaction_id += 1
        customer_id += random.randint(0, 5)  # Some customers repeat

    return pd.DataFrame(data)

# Generate datasets
train_df = generate_transactions(20000)  # ~100,000 rows (avg 5 items per transaction)
test_df = generate_transactions(4000, is_train=False)  # ~20,000 rows

# Save to CSV
train_df.to_csv("data/train.csv", index=False)
test_df.to_csv("data/test.csv", index=False)

# Generate sample submission
sample_submission = test_df[["transaction_id", "product_id"]].copy()
sample_submission["is_bundle_target"] = 0  # Dummy predictions
sample_submission.to_csv("data/sample_submission.csv", index=False)

print("Generated train.csv, test.csv, and sample_submission.csv")