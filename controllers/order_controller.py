from flask import Blueprint, render_template, request, session, make_response
from models.db import db
from models.models import TShirtCombination, Order, OrderItem
import uuid
import pdfkit

order_bp = Blueprint('order', __name__)

@order_bp.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        if Order.query.count() >= 200:
            return "Лимит заказов (2) исчерпан.", 403

        customer_name = request.form.get('customer_name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        email = request.form.get('email')
        card_data = request.form.get('card_data')
        order_code = str(uuid.uuid4())[:8]

        new_order = Order(
            order_code=order_code,
            customer_name=customer_name,
            phone=phone,
            address=address,
            email=email,
            card_data=card_data
        )
        db.session.add(new_order)
        db.session.commit()

        cart = session.get('cart', [])
        for item in cart:
            combination_id = item['combination_id']
            quantity = item['quantity']
            price = item['price']
            print_id = item['print_id']

            order_item = OrderItem(
                order_id=new_order.id,
                combination_id=combination_id,
                print_id=print_id,
                quantity=quantity,
                price=price
            )
            db.session.add(order_item)

            combination = TShirtCombination.query.get(combination_id)
            if combination:
                combination.stock -= quantity
                if combination.stock < 0:
                    combination.stock = 0
                db.session.add(combination)

        db.session.commit()
        session['cart'] = []
        session.modified = True

        rendered_html = render_template('order_pdf.html', order=new_order)
        config_pdf = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
        pdf = pdfkit.from_string(rendered_html, False, configuration=config_pdf)
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=order_{order_code}.pdf'
        return response

    return render_template('order.html')
