"""
Report Utilities
Helper functions for generating and formatting reports
"""

from datetime import datetime, timedelta
import csv
import io
from typing import List, Dict, Any


def format_currency(amount: float, currency: str = 'KES') -> str:
    """
    Format amount as currency string
    
    Args:
        amount: Amount to format
        currency: Currency code (default: KES)
    
    Returns:
        Formatted currency string
    """
    try:
        return f"{currency} {amount:,.2f}"
    except (TypeError, ValueError):
        return f"{currency} 0.00"


def calculate_growth_rate(current: float, previous: float) -> float:
    """
    Calculate growth rate percentage
    
    Args:
        current: Current period value
        previous: Previous period value
    
    Returns:
        Growth rate as percentage
    """
    if previous == 0:
        return 100.0 if current > 0 else 0.0
    
    try:
        growth = ((current - previous) / previous) * 100
        return round(growth, 2)
    except (TypeError, ValueError, ZeroDivisionError):
        return 0.0


def generate_date_range(start_date: datetime, end_date: datetime, period: str = 'day') -> List[datetime]:
    """
    Generate list of dates between start and end
    
    Args:
        start_date: Start date
        end_date: End date
        period: Period type ('day', 'week', 'month')
    
    Returns:
        List of datetime objects
    """
    dates = []
    current = start_date
    
    if period == 'day':
        delta = timedelta(days=1)
    elif period == 'week':
        delta = timedelta(weeks=1)
    elif period == 'month':
        delta = timedelta(days=30)  # Approximate
    else:
        delta = timedelta(days=1)
    
    while current <= end_date:
        dates.append(current)
        current += delta
    
    return dates


def export_to_csv(data: List[Dict[str, Any]], filename: str = 'report.csv') -> str:
    """
    Export data to CSV format
    
    Args:
        data: List of dictionaries to export
        filename: Output filename
    
    Returns:
        CSV string
    """
    if not data:
        return ""
    
    output = io.StringIO()
    
    # Get headers from first row
    headers = list(data[0].keys())
    
    writer = csv.DictWriter(output, fieldnames=headers)
    writer.writeheader()
    writer.writerows(data)
    
    return output.getvalue()


def aggregate_by_period(data: List[Dict[str, Any]], date_field: str, period: str = 'day') -> Dict[str, List[Dict[str, Any]]]:
    """
    Group data by time period
    
    Args:
        data: List of data dictionaries
        date_field: Field name containing date
        period: Period type ('day', 'week', 'month')
    
    Returns:
        Dictionary with period keys and data lists
    """
    aggregated = {}
    
    for item in data:
        date_value = item.get(date_field)
        
        if not date_value:
            continue
        
        # Convert to datetime if string
        if isinstance(date_value, str):
            try:
                date_value = datetime.fromisoformat(date_value.replace('Z', '+00:00'))
            except ValueError:
                continue
        
        # Generate period key
        if period == 'day':
            key = date_value.strftime('%Y-%m-%d')
        elif period == 'week':
            key = date_value.strftime('%Y-W%W')
        elif period == 'month':
            key = date_value.strftime('%Y-%m')
        else:
            key = date_value.strftime('%Y-%m-%d')
        
        if key not in aggregated:
            aggregated[key] = []
        
        aggregated[key].append(item)
    
    return aggregated


def calculate_percentage(part: float, total: float) -> float:
    """
    Calculate percentage
    
    Args:
        part: Part value
        total: Total value
    
    Returns:
        Percentage value
    """
    if total == 0:
        return 0.0
    
    try:
        return round((part / total) * 100, 2)
    except (TypeError, ValueError, ZeroDivisionError):
        return 0.0


def format_date_range(start_date: datetime, end_date: datetime) -> str:
    """
    Format date range as string
    
    Args:
        start_date: Start date
        end_date: End date
    
    Returns:
        Formatted date range string
    """
    return f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers
    
    Args:
        numerator: Numerator
        denominator: Denominator
        default: Default value if division fails
    
    Returns:
        Division result or default
    """
    try:
        if denominator == 0:
            return default
        return round(numerator / denominator, 2)
    except (TypeError, ValueError, ZeroDivisionError):
        return default
