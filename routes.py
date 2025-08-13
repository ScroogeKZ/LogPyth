from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from sqlalchemy import func, desc, and_
import json

from app import app, db
from models import User, Order, Driver
from forms import OrderForm, TrackingForm, RegistrationForm, LoginForm, OrderEditForm, DriverForm
from utils import generate_tracking_number, send_telegram_notification
from telegram_bot import send_order_notification

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/order/<shipping_type>', methods=['GET', 'POST'])
def create_order(shipping_type):
    if shipping_type not in ['astana', 'kazakhstan']:
        flash('Недопустимый тип отгрузки', 'error')
        return redirect(url_for('index'))
    
    form = OrderForm()
    
    if form.validate_on_submit():
        # Generate unique tracking number
        tracking_number = generate_tracking_number()
        
        # Create new order
        order = Order(
            tracking_number=tracking_number,
            customer_name=form.customer_name.data,
            customer_phone=form.customer_phone.data,
            customer_email=form.customer_email.data,
            shipping_type=shipping_type,
            pickup_address=form.pickup_address.data,
            pickup_contact=form.pickup_contact.data,
            delivery_address=form.delivery_address.data,
            delivery_contact=form.delivery_contact.data,
            cargo_description=form.cargo_description.data,
            cargo_weight=form.cargo_weight.data,
            cargo_dimensions=form.cargo_dimensions.data,
            customer_notes=form.customer_notes.data,
            status='new'
        )
        
        # Link to user if logged in
        if current_user.is_authenticated:
            order.customer_id = current_user.id
        
        db.session.add(order)
        db.session.commit()
        
        # Send Telegram notification
        send_order_notification(order)
        
        flash(f'Ваша заявка принята! Номер отслеживания: {tracking_number}', 'success')
        return redirect(url_for('track_order', tracking_number=tracking_number))
    
    shipping_title = 'Отгрузка по Астане' if shipping_type == 'astana' else 'Отгрузка по Казахстану'
    return render_template('order_form.html', form=form, shipping_type=shipping_type, shipping_title=shipping_title)

@app.route('/track')
@app.route('/track/<tracking_number>')
def track_order(tracking_number=None):
    form = TrackingForm()
    order = None
    
    if tracking_number:
        order = Order.query.filter_by(tracking_number=tracking_number).first()
        if not order:
            flash('Заказ с указанным номером не найден', 'error')
    
    return render_template('track_order.html', form=form, order=order, tracking_number=tracking_number)

@app.route('/track_search', methods=['POST'])
def track_search():
    form = TrackingForm()
    if form.validate_on_submit():
        return redirect(url_for('track_order', tracking_number=form.tracking_number.data))
    return redirect(url_for('track_order'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        # Check if username or email already exists
        existing_user = User.query.filter(
            (User.username == form.username.data) | (User.email == form.email.data)
        ).first()
        
        if existing_user:
            flash('Пользователь с таким именем или email уже существует', 'error')
            return render_template('register.html', form=form)
        
        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data,
            full_name=form.full_name.data,
            phone=form.phone.data,
            password_hash=generate_password_hash(form.password.data),
            role='employee'
        )
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        flash('Регистрация успешно завершена!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Вы успешно вошли в систему!', 'success')
            
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Неверное имя пользователя или пароль', 'error')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    # Get user's orders
    orders = Order.query.filter_by(customer_id=current_user.id).order_by(desc(Order.created_at)).all()
    return render_template('profile.html', orders=orders)

# Admin routes
@app.route('/admin')
@login_required
def admin_dashboard():
    # Get basic statistics
    total_orders = Order.query.count()
    new_orders = Order.query.filter_by(status='new').count()
    in_progress_orders = Order.query.filter_by(status='in_progress').count()
    delivered_orders = Order.query.filter_by(status='delivered').count()
    
    # Recent orders
    recent_orders = Order.query.order_by(desc(Order.created_at)).limit(10).all()
    
    # Revenue statistics
    total_revenue = db.session.query(func.sum(Order.price)).filter(Order.price.isnot(None)).scalar() or 0
    avg_order_value = db.session.query(func.avg(Order.price)).filter(Order.price.isnot(None)).scalar() or 0
    
    return render_template('admin/dashboard.html',
                         total_orders=total_orders,
                         new_orders=new_orders,
                         in_progress_orders=in_progress_orders,
                         delivered_orders=delivered_orders,
                         recent_orders=recent_orders,
                         total_revenue=total_revenue,
                         avg_order_value=avg_order_value)

@app.route('/admin/orders')
@login_required
def admin_orders():
    # Filter parameters
    status_filter = request.args.get('status', '')
    shipping_type_filter = request.args.get('shipping_type', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    
    # Build query
    query = Order.query
    
    # Apply filters based on user role
    if current_user.role == 'employee':
        query = query.filter_by(customer_id=current_user.id)
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    if shipping_type_filter:
        query = query.filter_by(shipping_type=shipping_type_filter)
    
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
            query = query.filter(Order.created_at >= date_from_obj)
        except ValueError:
            pass
    
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d') + timedelta(days=1)
            query = query.filter(Order.created_at < date_to_obj)
        except ValueError:
            pass
    
    orders = query.order_by(desc(Order.created_at)).all()
    
    return render_template('admin/orders.html', orders=orders,
                         status_filter=status_filter,
                         shipping_type_filter=shipping_type_filter,
                         date_from=date_from,
                         date_to=date_to)

@app.route('/admin/orders/<int:order_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_order(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Check permissions
    if current_user.role == 'employee' and order.customer_id != current_user.id:
        flash('У вас нет прав для редактирования этого заказа', 'error')
        return redirect(url_for('admin_orders'))
    
    form = OrderEditForm()
    
    # Populate driver choices
    drivers = Driver.query.filter_by(is_active=True).all()
    form.driver_id.choices = [(0, 'Не назначен')] + [(d.id, f'{d.name} ({d.phone})') for d in drivers]
    
    if form.validate_on_submit():
        # Update order fields based on user role
        if current_user.role == 'logist':
            order.status = form.status.data
            order.price = form.price.data
            order.driver_id = form.driver_id.data if form.driver_id.data != 0 else None
            order.internal_comments = form.internal_comments.data
        
        # Both roles can update contact info
        order.customer_phone = form.customer_phone.data
        order.customer_email = form.customer_email.data
        order.pickup_address = form.pickup_address.data
        order.pickup_contact = form.pickup_contact.data
        order.delivery_address = form.delivery_address.data
        order.delivery_contact = form.delivery_contact.data
        order.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Заказ успешно обновлен!', 'success')
        return redirect(url_for('admin_orders'))
    
    # Pre-populate form
    if request.method == 'GET':
        form.status.data = order.status
        form.price.data = order.price
        form.driver_id.data = order.driver_id or 0
        form.internal_comments.data = order.internal_comments
        form.customer_phone.data = order.customer_phone
        form.customer_email.data = order.customer_email
        form.pickup_address.data = order.pickup_address
        form.pickup_contact.data = order.pickup_contact
        form.delivery_address.data = order.delivery_address
        form.delivery_contact.data = order.delivery_contact
    
    return render_template('admin/edit_order.html', form=form, order=order)

@app.route('/admin/analytics')
@login_required
def analytics():
    if current_user.role != 'logist':
        flash('У вас нет доступа к аналитике', 'error')
        return redirect(url_for('admin_dashboard'))
    
    # Date range for analytics (last 30 days by default)
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=30)
    
    # Orders by status
    status_stats = db.session.query(
        Order.status,
        func.count(Order.id).label('count')
    ).filter(Order.created_at >= start_date).group_by(Order.status).all()
    
    # Orders by shipping type
    shipping_stats = db.session.query(
        Order.shipping_type,
        func.count(Order.id).label('count'),
        func.sum(Order.price).label('revenue')
    ).filter(Order.created_at >= start_date).group_by(Order.shipping_type).all()
    
    # Daily orders for the last 30 days
    daily_orders = db.session.query(
        func.date(Order.created_at).label('date'),
        func.count(Order.id).label('count'),
        func.sum(Order.price).label('revenue')
    ).filter(Order.created_at >= start_date).group_by(func.date(Order.created_at)).all()
    
    # Driver performance
    driver_stats = db.session.query(
        Driver.name,
        func.count(Order.id).label('orders_count'),
        func.sum(Order.price).label('total_revenue')
    ).join(Order, Driver.id == Order.driver_id).filter(
        Order.created_at >= start_date
    ).group_by(Driver.id, Driver.name).all()
    
    # Cost analysis
    total_revenue = db.session.query(func.sum(Order.price)).filter(
        and_(Order.created_at >= start_date, Order.price.isnot(None))
    ).scalar() or 0
    
    avg_order_value = db.session.query(func.avg(Order.price)).filter(
        and_(Order.created_at >= start_date, Order.price.isnot(None))
    ).scalar() or 0
    
    total_orders = Order.query.filter(Order.created_at >= start_date).count()
    
    return render_template('admin/analytics.html',
                         status_stats=status_stats,
                         shipping_stats=shipping_stats,
                         daily_orders=daily_orders,
                         driver_stats=driver_stats,
                         total_revenue=total_revenue,
                         avg_order_value=avg_order_value,
                         total_orders=total_orders,
                         start_date=start_date,
                         end_date=end_date)

@app.route('/admin/analytics/data')
@login_required
def analytics_data():
    """API endpoint for chart data"""
    if current_user.role != 'logist':
        return jsonify({'error': 'Access denied'}), 403
    
    # Get data for charts
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=30)
    
    # Daily orders data
    daily_data = db.session.query(
        func.date(Order.created_at).label('date'),
        func.count(Order.id).label('orders'),
        func.coalesce(func.sum(Order.price), 0).label('revenue')
    ).filter(Order.created_at >= start_date).group_by(func.date(Order.created_at)).all()
    
    # Status distribution
    status_data = db.session.query(
        Order.status,
        func.count(Order.id).label('count')
    ).filter(Order.created_at >= start_date).group_by(Order.status).all()
    
    return jsonify({
        'daily_orders': [
            {
                'date': str(row.date),
                'orders': row.orders,
                'revenue': float(row.revenue or 0)
            } for row in daily_data
        ],
        'status_distribution': [
            {
                'status': row.status,
                'count': row.count,
                'label': Order().get_status_display() if hasattr(Order(), 'get_status_display') else row.status
            } for row in status_data
        ]
    })

# Driver management routes
@app.route('/admin/drivers')
@login_required
def admin_drivers():
    if current_user.role != 'logist':
        flash('У вас нет доступа к управлению водителями', 'error')
        return redirect(url_for('admin_dashboard'))
    
    drivers = Driver.query.all()
    return render_template('admin/drivers.html', drivers=drivers)

@app.route('/admin/drivers/new', methods=['GET', 'POST'])
@login_required
def add_driver():
    if current_user.role != 'logist':
        flash('У вас нет прав для добавления водителей', 'error')
        return redirect(url_for('admin_dashboard'))
    
    form = DriverForm()
    
    if form.validate_on_submit():
        driver = Driver(
            name=form.name.data,
            phone=form.phone.data,
            vehicle_info=form.vehicle_info.data
        )
        
        db.session.add(driver)
        db.session.commit()
        
        flash('Водитель успешно добавлен!', 'success')
        return redirect(url_for('admin_drivers'))
    
    return render_template('admin/edit_driver.html', form=form, driver=None)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
