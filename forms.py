from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FloatField, PasswordField, EmailField, TelField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange

class OrderForm(FlaskForm):
    customer_name = StringField('Ф.И.О.', validators=[DataRequired(), Length(min=2, max=100)])
    customer_phone = TelField('Номер телефона', validators=[DataRequired(), Length(min=10, max=20)])
    customer_email = EmailField('Email', validators=[Optional(), Email()])
    
    pickup_address = TextAreaField('Адрес погрузки', validators=[DataRequired(), Length(min=5, max=500)])
    pickup_contact = StringField('Контактное лицо на погрузке', validators=[Optional(), Length(max=200)])
    
    delivery_address = TextAreaField('Адрес выгрузки', validators=[DataRequired(), Length(min=5, max=500)])
    delivery_contact = StringField('Контактное лицо на выгрузке', validators=[Optional(), Length(max=200)])
    
    cargo_description = TextAreaField('Описание груза', validators=[DataRequired(), Length(min=5, max=1000)])
    cargo_weight = FloatField('Вес груза (кг)', validators=[Optional(), NumberRange(min=0)])
    cargo_dimensions = StringField('Габариты груза', validators=[Optional(), Length(max=100)])
    
    customer_notes = TextAreaField('Дополнительные комментарии', validators=[Optional(), Length(max=500)])

class TrackingForm(FlaskForm):
    tracking_number = StringField('Номер отслеживания', validators=[DataRequired(), Length(min=5, max=20)])

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3, max=64)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    full_name = StringField('Полное имя', validators=[DataRequired(), Length(min=2, max=100)])
    phone = TelField('Номер телефона', validators=[DataRequired(), Length(min=10, max=20)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])

class OrderEditForm(FlaskForm):
    status = SelectField('Статус', choices=[
        ('new', 'Новая заявка'),
        ('confirmed', 'Подтверждена'),
        ('in_progress', 'В пути'),
        ('delivered', 'Доставлена'),
        ('cancelled', 'Отменена')
    ], validators=[DataRequired()])
    
    price = FloatField('Цена', validators=[Optional(), NumberRange(min=0)])
    driver_id = SelectField('Водитель', coerce=int, validators=[Optional()])
    internal_comments = TextAreaField('Внутренние комментарии', validators=[Optional(), Length(max=1000)])
    
    # Allow editing of contact info and addresses
    customer_phone = TelField('Номер телефона', validators=[DataRequired(), Length(min=10, max=20)])
    customer_email = EmailField('Email', validators=[Optional(), Email()])
    pickup_address = TextAreaField('Адрес погрузки', validators=[DataRequired(), Length(min=5, max=500)])
    pickup_contact = StringField('Контактное лицо на погрузке', validators=[Optional(), Length(max=200)])
    delivery_address = TextAreaField('Адрес выгрузки', validators=[DataRequired(), Length(min=5, max=500)])
    delivery_contact = StringField('Контактное лицо на выгрузке', validators=[Optional(), Length(max=200)])

class DriverForm(FlaskForm):
    name = StringField('Имя водителя', validators=[DataRequired(), Length(min=2, max=100)])
    phone = TelField('Номер телефона', validators=[DataRequired(), Length(min=10, max=20)])
    vehicle_info = StringField('Информация о транспорте', validators=[Optional(), Length(max=200)])
