from datetime import datetime
from app import db
from flask_login import UserMixin
from sqlalchemy import Text

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='employee')  # employee, logist
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to orders
    orders = db.relationship('Order', backref='customer', lazy=True, foreign_keys='Order.customer_id')

class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    vehicle_info = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to orders
    orders = db.relationship('Order', backref='assigned_driver', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tracking_number = db.Column(db.String(20), unique=True, nullable=False)
    
    # Customer information
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    customer_email = db.Column(db.String(120))
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # For registered users
    
    # Shipping type and addresses
    shipping_type = db.Column(db.String(20), nullable=False)  # astana, kazakhstan
    pickup_address = db.Column(Text, nullable=False)
    pickup_contact = db.Column(db.String(200))
    delivery_address = db.Column(Text, nullable=False)
    delivery_contact = db.Column(db.String(200))
    
    # Cargo information
    cargo_description = db.Column(Text, nullable=False)
    cargo_weight = db.Column(db.Float)
    cargo_dimensions = db.Column(db.String(100))
    
    # Order management
    status = db.Column(db.String(30), default='new')  # new, confirmed, in_progress, delivered, cancelled
    price = db.Column(db.Float)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=True)
    
    # Comments and notes
    customer_notes = db.Column(Text)
    internal_comments = db.Column(Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_status_display(self):
        status_map = {
            'new': 'Новая заявка',
            'confirmed': 'Подтверждена',
            'in_progress': 'В пути',
            'delivered': 'Доставлена',
            'cancelled': 'Отменена'
        }
        return status_map.get(self.status, self.status)
    
    def get_shipping_type_display(self):
        type_map = {
            'astana': 'Отгрузка по Астане',
            'kazakhstan': 'Отгрузка по Казахстану'
        }
        return type_map.get(self.shipping_type, self.shipping_type)
