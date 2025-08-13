import os
from utils import send_telegram_notification

def send_order_notification(order):
    """Send new order notification to Telegram"""
    message = f"""
🚚 <b>Новая заявка #{order.tracking_number}</b>

👤 <b>Клиент:</b> {order.customer_name}
📱 <b>Телефон:</b> {order.customer_phone}
📧 <b>Email:</b> {order.customer_email or 'Не указан'}

📍 <b>Тип доставки:</b> {order.get_shipping_type_display()}

📦 <b>Описание груза:</b> {order.cargo_description}
⚖️ <b>Вес:</b> {order.cargo_weight or 'Не указан'} кг
📏 <b>Габариты:</b> {order.cargo_dimensions or 'Не указаны'}

🏠 <b>Адрес погрузки:</b> {order.pickup_address}
🏢 <b>Адрес выгрузки:</b> {order.delivery_address}

📝 <b>Комментарии:</b> {order.customer_notes or 'Нет'}

⏰ <b>Время создания:</b> {order.created_at.strftime('%d.%m.%Y %H:%M')}
    """
    
    return send_telegram_notification(message.strip())

def send_status_update(order, old_status, new_status):
    """Send order status update notification"""
    status_map = {
        'new': 'Новая заявка',
        'confirmed': 'Подтверждена',
        'in_progress': 'В пути',
        'delivered': 'Доставлена',
        'cancelled': 'Отменена'
    }
    
    message = f"""
📊 <b>Изменение статуса заказа #{order.tracking_number}</b>

👤 <b>Клиент:</b> {order.customer_name}
📱 <b>Телефон:</b> {order.customer_phone}

📈 <b>Статус изменен:</b> {status_map.get(old_status, old_status)} → {status_map.get(new_status, new_status)}

💰 <b>Цена:</b> {f'{order.price} ₸' if order.price else 'Не назначена'}
🚛 <b>Водитель:</b> {order.assigned_driver.name if order.assigned_driver else 'Не назначен'}
    """
    
    return send_telegram_notification(message.strip())
