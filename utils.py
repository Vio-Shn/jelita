from datetime import datetime, timedelta

def get_order_status_badge(status):
    """Return badge color and text for order status"""
    status_map = {
        'pending': {'color': 'yellow', 'text': 'Menunggu Pembayaran'},
        'paid': {'color': 'blue', 'text': 'Dibayar'},
        'processing': {'color': 'blue', 'text': 'Diproses'},
        'shipped': {'color': 'indigo', 'text': 'Dikirim'},
        'delivered': {'color': 'green', 'text': 'Terkirim'},
        'cancelled': {'color': 'red', 'text': 'Dibatalkan'}
    }
    return status_map.get(status, {'color': 'gray', 'text': 'Unknown'})


def get_payment_status_badge(status):
    """Return badge color and text for payment status"""
    status_map = {
        'unpaid': {'color': 'red', 'text': 'Belum Dibayar'},
        'paid': {'color': 'green', 'text': 'Sudah Dibayar'}
    }
    return status_map.get(status, {'color': 'gray', 'text': 'Unknown'})


def format_currency(amount):
    """Format currency to Indonesian Rupiah"""
    return f"Rp {amount:,.0f}".replace(',', '.')


def calculate_estimated_delivery(order_date, days=7):
    """Calculate estimated delivery date"""
    return order_date + timedelta(days=days)
