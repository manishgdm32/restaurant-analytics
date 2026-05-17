import pandas as pd
import numpy as np
from src.data_loader import load_all_data

_data = None

def get_data():
    global _data
    if _data is None:
        _data = load_all_data()
    return _data

def load_all_data():
    from src.data_loader import load_all_data as loader
    return loader()

data = get_data()
orders = data['valid_orders']
items = data['items']

def get_kpis():
    """Return key performance indicators"""
    total_revenue = orders['Amount'].sum()
    total_orders = len(orders)
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    total_tips = orders['Tip'].sum()
    tip_percentage = (total_tips / total_revenue * 100) if total_revenue > 0 else 0
    total_taxes = orders['Tax'].sum()

    return {
        'total_revenue': round(total_revenue, 2),
        'total_orders': total_orders,
        'avg_order_value': round(avg_order_value, 2),
        'total_tips': round(total_tips, 2),
        'tip_percentage': round(tip_percentage, 2),
        'total_taxes': round(total_taxes, 2)
    }

def get_daily_sales():
    """Daily revenue trend"""
    daily = orders.groupby('Date')['Amount'].sum().reset_index()
    daily['Date'] = pd.to_datetime(daily['Date'])
    return daily.sort_values('Date')

def get_hourly_sales():
    """Hourly sales distribution"""
    hourly = orders.groupby('Hour')['Amount'].sum().reset_index()
    return hourly

def get_daily_by_dayofweek():
    """Sales by day of week"""
    dow = orders.groupby('DayOfWeek')['Amount'].sum().reindex([
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
    ])
    return dow

def get_top_items(limit=15):
    """Top selling items by revenue"""
    valid_items = items[items['Void?'] == False]
    top = valid_items.groupby('Menu Item')['Net Price'].sum().sort_values(ascending=False).head(limit)
    return top

def get_category_sales():
    """Sales by category"""
    valid_items = items[items['Void?'] == False]
    cat = valid_items.groupby('Sales Category')['Net Price'].sum().sort_values(ascending=False)
    return cat

def get_discount_impact():
    """Discount effectiveness analysis"""
    disc = data['discount_sales']
    summary = disc.groupby('Dining Option').agg({
        'Net Sales': 'sum',
        'Discount Amount': 'sum',
        'Item Qty': 'sum'
    }).reset_index()
    summary['Discount %'] = (summary['Discount Amount'] / summary['Net Sales'] * 100).round(2)
    return summary

def get_channel_performance():
    """Dine-in vs Takeout vs DoorDash"""
    channel = data['discount_sales'].groupby('Dining Option').agg({
        'Net Sales': 'sum',
        'Item Qty': 'sum'
    }).reset_index()
    channel['Avg Order Value'] = (channel['Net Sales'] / channel['Item Qty']).round(2)
    return channel.sort_values('Net Sales', ascending=False)

def get_server_performance():
    """Performance by server"""
    server = orders.groupby('Server').agg({
        'Amount': 'sum',
        'Order #': 'count',
        'Tip': 'sum'
    }).reset_index()
    server.columns = ['Server', 'Revenue', 'Orders', 'Tips']
    server['Avg Order'] = (server['Revenue'] / server['Orders']).round(2)
    return server.sort_values('Revenue', ascending=False)

def get_menu_group_performance():
    """Performance by menu group"""
    valid_items = items[items['Void?'] == False]
    group = valid_items.groupby('Menu Group')['Net Price'].sum().sort_values(ascending=False)
    return group

def get_payout_summary():
    """Payout overview"""
    payout = data['payouts']
    return {
        'total_payments': payout['Payments'].sum(),
        'total_fees': payout['Fees'].sum(),
        'total_payouts': payout['Payouts'].sum(),
        'avg_daily_payout': round(payout['Payouts'].mean(), 2)
    }

def get_ai_context():
    """Prepare context for AI chatbot"""
    kpis = get_kpis()
    top_items = get_top_items(10)
    hourly = get_hourly_sales()
    channel = get_channel_performance()
    discount = get_discount_impact()

    context = f"""
RESTAURANT ANALYTICS SUMMARY - LOTA INDIAN CUISINE - APRIL 2026
{'='*60}

KEY METRICS:
- Total Revenue: ${kpis['total_revenue']:,.2f}
- Total Orders: {kpis['total_orders']}
- Average Order Value: ${kpis['avg_order_value']:.2f}
- Total Tips: ${kpis['total_tips']:.2f} ({kpis['tip_percentage']}% of revenue)
- Total Taxes: ${kpis['total_taxes']:.2f}

TOP 10 SELLING ITEMS (by revenue):
{top_items.to_string()}

HOURLY SALES DISTRIBUTION:
{hourly.to_string()}

CHANNEL PERFORMANCE:
{channel.to_string()}

DISCOUNT IMPACT:
{discount.to_string()}

PEAK HOURS: 12-2 PM (lunch) and 6-9 PM (dinner)
BEST PERFORMING CHANNEL: Dine-in
TOP CATEGORY: Food (main entrees)
"""
    return context

__all__ = [
    'get_data', 'get_kpis', 'get_daily_sales', 'get_hourly_sales', 'get_daily_by_dayofweek',
    'get_top_items', 'get_category_sales', 'get_discount_impact',
    'get_channel_performance', 'get_server_performance', 'get_menu_group_performance',
    'get_payout_summary', 'get_ai_context'
]