from datetime import datetime
from models.db import db

class TShirtModel(db.Model):
    __tablename__ = 'tshirt_models'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    base_image = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Float, default=0.0)

    def __repr__(self):
        return f"<TShirtModel {self.name}>"

class Color(db.Model):
    __tablename__ = 'colors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    hex_code = db.Column(db.String(7), nullable=True)

    def __repr__(self):
        return f"<Color {self.name}>"

class Size(db.Model):
    __tablename__ = 'sizes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"<Size {self.name}>"

class Print(db.Model):
    __tablename__ = 'prints'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"<Print {self.name}>"

class TShirtCombination(db.Model):
    """
    Сочетание модель + цвет + размер
    """
    __tablename__ = 'tshirt_combinations'
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('tshirt_models.id'), nullable=False)
    color_id = db.Column(db.Integer, db.ForeignKey('colors.id'), nullable=False)
    size_id = db.Column(db.Integer, db.ForeignKey('sizes.id'), nullable=False)
    stock = db.Column(db.Integer, default=0)
    combination_image = db.Column(db.String(200), nullable=True)

    model = db.relationship('TShirtModel', backref='combinations')
    color = db.relationship('Color', backref='combinations')
    size = db.relationship('Size', backref='combinations')

    def __repr__(self):
        return f"<TShirtCombination {self.model.name} / {self.color.name} / {self.size.name}>"

class PrintCompatibility(db.Model):
    """
    Связь: какие принты совместимы с конкретной комбинацией
    """
    __tablename__ = 'print_compatibility'
    id = db.Column(db.Integer, primary_key=True)
    combination_id = db.Column(db.Integer, db.ForeignKey('tshirt_combinations.id'), nullable=False)
    print_id = db.Column(db.Integer, db.ForeignKey('prints.id'), nullable=False)

    combination = db.relationship('TShirtCombination', backref='compatible_prints')
    print_obj = db.relationship('Print', backref='compatible_combinations')

    def __repr__(self):
        return f"<PrintCompatibility Comb:{self.combination_id} Print:{self.print_id}>"

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_code = db.Column(db.String(36), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    customer_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    card_data = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"<Order {self.order_code}>"

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    combination_id = db.Column(db.Integer, db.ForeignKey('tshirt_combinations.id'), nullable=False)
    print_id = db.Column(db.Integer, db.ForeignKey('prints.id'), nullable=True)
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Float, default=0.0)

    order = db.relationship('Order', backref='items')
    combination = db.relationship('TShirtCombination')
    print_obj = db.relationship('Print')

    def __repr__(self):
        return f"<OrderItem Order:{self.order_id} Comb:{self.combination_id}>"
