import random
import string
import requests
import os
from datetime import datetime

def generate_tracking_number():
    """Generate a unique tracking number"""
    timestamp = datetime.now().strftime('%y%m%d')
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f'HK{timestamp}{random_part}'

def send_sms_notification(phone, message):
    """Send SMS notification (placeholder for SMS service integration)"""
    # This would integrate with an SMS service like SMS.ru, SMSC.ru, etc.
    # For now, we'll just log the message
    print(f"SMS to {phone}: {message}")
    return True

def format_phone_number(phone):
    """Format phone number for display"""
    # Remove all non-digit characters
    digits_only = ''.join(filter(str.isdigit, phone))
    
    # Format as +7 (XXX) XXX-XX-XX for Kazakhstan numbers
    if digits_only.startswith('7') and len(digits_only) == 11:
        return f"+7 ({digits_only[1:4]}) {digits_only[4:7]}-{digits_only[7:9]}-{digits_only[9:11]}"
    elif digits_only.startswith('8') and len(digits_only) == 11:
        return f"+7 ({digits_only[1:4]}) {digits_only[4:7]}-{digits_only[7:9]}-{digits_only[9:11]}"
    else:
        return phone

def format_currency(amount):
    """Format currency amount in Tenge"""
    if amount is None:
        return "Не указана"
    return f"{amount:,.0f} ₸"

def send_telegram_notification(message):
    """Send notification to Telegram channel/group"""
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        print(f"Telegram notification: {message}")
        return False
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    try:
        response = requests.post(url, data=data, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Failed to send Telegram notification: {e}")
        return False
