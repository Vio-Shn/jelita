import requests
import json
from datetime import datetime
import os
import hashlib
import hmac
import base64

class MidtransPayment:
    """Handle Midtrans payment processing using REST API"""
    
    SERVER_KEY = os.environ.get('MIDTRANS_SERVER_KEY', 'your-server-key-here')
    CLIENT_KEY = os.environ.get('MIDTRANS_CLIENT_KEY', 'your-client-key-here')
    ENVIRONMENT = os.environ.get('MIDTRANS_ENVIRONMENT', 'sandbox')
    
    # Midtrans API endpoints
    if ENVIRONMENT == 'production':
        SNAP_URL = 'https://app.midtrans.com/snap/v1/transactions'
        API_URL = 'https://app.midtrans.com/api/v1'
    else:
        SNAP_URL = 'https://app.sandbox.midtrans.com/snap/v1/transactions'
        API_URL = 'https://app.sandbox.midtrans.com/api/v1'
    
    @staticmethod
    def _get_auth_header():
        """Generate basic auth header for Midtrans API"""
        auth_string = MidtransPayment.SERVER_KEY + ':'
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')
        return f'Basic {auth_base64}'
    
    @staticmethod
    def create_transaction(order):
        """Create Midtrans transaction for order"""
        try:
            transaction_details = {
                'order_id': order.order_number,
                'gross_amount': int(order.total_amount)
            }
            
            item_details = []
            for item in order.items:
                item_details.append({
                    'id': str(item.product_id),
                    'price': int(item.price),
                    'quantity': item.quantity,
                    'name': item.product.name
                })
            
            if order.tax_amount > 0:
                item_details.append({
                    'id': 'tax',
                    'price': int(order.tax_amount),
                    'quantity': 1,
                    'name': 'Pajak (Tax)'
                })
            
            if order.shipping_cost > 0:
                item_details.append({
                    'id': 'shipping',
                    'price': int(order.shipping_cost),
                    'quantity': 1,
                    'name': 'Pengiriman (Shipping)'
                })
            
            customer_details = {
                'first_name': order.user.username,
                'email': order.user.email,
                'phone': order.user.phone or '0'
            }
            
            payload = {
                'transaction_details': transaction_details,
                'item_details': item_details,
                'customer_details': customer_details
            }
            
            # Create transaction via Midtrans Snap API
            headers = {
                'Authorization': MidtransPayment._get_auth_header(),
                'Content-Type': 'application/json'
            }
            
            response = requests.post(
                MidtransPayment.SNAP_URL,
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 201:
                result = response.json()
                return {
                    'status': 'success',
                    'token': result.get('token'),
                    'redirect_url': result.get('redirect_url'),
                    'transaction_id': result.get('id')
                }
            else:
                return {
                    'status': 'error',
                    'message': f'Midtrans API error: {response.status_code}'
                }
        except requests.exceptions.RequestException as e:
            return {
                'status': 'error',
                'message': f'Connection error: {str(e)}'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    @staticmethod
    def verify_payment(order_id):
        """Verify payment status from Midtrans"""
        try:
            # Verify payment status via Midtrans API
            headers = {
                'Authorization': MidtransPayment._get_auth_header(),
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f'{MidtransPayment.API_URL}/transactions/{order_id}/status',
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'status': 'success',
                    'transaction_status': result.get('transaction_status'),
                    'payment_type': result.get('payment_type'),
                    'gross_amount': result.get('gross_amount')
                }
            else:
                return {
                    'status': 'error',
                    'message': f'Midtrans API error: {response.status_code}'
                }
        except requests.exceptions.RequestException as e:
            return {
                'status': 'error',
                'message': f'Connection error: {str(e)}'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    @staticmethod
    def handle_notification(notification_obj):
        """Handle Midtrans notification webhook"""
        try:
            order_id = notification_obj.get('order_id')
            transaction_status = notification_obj.get('transaction_status')
            payment_type = notification_obj.get('payment_type')
            transaction_id = notification_obj.get('transaction_id')
            
            signature_key = notification_obj.get('signature_key')
            server_key = MidtransPayment.SERVER_KEY
            
            # Create expected signature
            status_code = notification_obj.get('status_code', '')
            order_id_str = str(order_id)
            gross_amount_str = str(int(notification_obj.get('gross_amount', 0)))
            
            data_to_sign = f'{order_id_str}{status_code}{gross_amount_str}{server_key}'
            expected_signature = hashlib.sha512(data_to_sign.encode()).hexdigest()
            
            # Verify signature
            if signature_key != expected_signature:
                return {
                    'status': 'error',
                    'message': 'Invalid signature'
                }
            
            return {
                'order_id': order_id,
                'transaction_status': transaction_status,
                'payment_type': payment_type,
                'transaction_id': transaction_id,
                'status': 'success'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
