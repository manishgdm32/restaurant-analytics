import pandas as pd
import os
from datetime import datetime

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw")

def load_all_data():
    """Load all CSV files and return merged dataset"""

    orders = pd.read_csv(f"{DATA_PATH}\\OrderDetails_2026_04_01-2026_04_30.csv", encoding='latin-1')
    items = pd.read_csv(f"{DATA_PATH}\\ItemSelectionDetails_2026_04_01-2026_04_30.csv", encoding='latin-1')
    category_sales = pd.read_csv(f"{DATA_PATH}\\sales-breakdown-apr1-30-2026 - Dining-Sales Categlory.csv", encoding='latin-1')
    discount_sales = pd.read_csv(f"{DATA_PATH}\\sales-breakdown-apr1-30-2026 Discount.csv", encoding='latin-1')
    payouts = pd.read_csv(f"{DATA_PATH}\\Payout overview.csv", encoding='latin-1')

    orders['Opened'] = pd.to_datetime(orders['Opened'], format='mixed')
    orders['Date'] = orders['Opened'].dt.date
    orders['Hour'] = orders['Opened'].dt.hour
    orders['DayOfWeek'] = orders['Opened'].dt.day_name()
    orders['DayNum'] = orders['Opened'].dt.day

    items['Sent Date'] = pd.to_datetime(items['Sent Date'], format='mixed')

    merged = items.merge(orders, left_on='Order #', right_on='Order #', how='left', suffixes=('_item', '_order'))

    valid_orders = orders[orders['Voided'] == False]

    return {
        'orders': orders,
        'valid_orders': valid_orders,
        'items': items,
        'category_sales': category_sales,
        'discount_sales': discount_sales,
        'payouts': payouts,
        'merged': merged
    }

if __name__ == "__main__":
    data = load_all_data()
    print(f"Loaded {len(data['orders'])} orders, {len(data['items'])} items")