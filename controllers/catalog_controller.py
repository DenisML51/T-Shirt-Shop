from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from models.models import TShirtModel, Color, Size, Print, TShirtCombination, PrintCompatibility

catalog_bp = Blueprint('catalog', __name__)

@catalog_bp.route('/catalog', methods=['GET'])
def catalog():
    if 'cart' not in session:
        session['cart'] = []

    tshirt_models = TShirtModel.query.all()
    colors = Color.query.all()
    sizes = Size.query.all()
    # Используем все принты для AJAX-подгрузки совместимых вариантов
    prints = Print.query.all()

    return render_template(
        'catalog.html',
        tshirt_models=tshirt_models,
        colors=colors,
        sizes=sizes,
        prints=prints,
        cart=session['cart']
    )

@catalog_bp.route('/get_prints', methods=['POST'])
def get_prints():
    model_id = request.form.get('model_id')
    color_id = request.form.get('color_id')
    size_id = request.form.get('size_id')

    combination = TShirtCombination.query.filter_by(
        model_id=model_id,
        color_id=color_id,
        size_id=size_id
    ).first()

    if not combination:
        return jsonify([])

    compat = PrintCompatibility.query.filter_by(combination_id=combination.id).all()
    result = [{
        'print_id': c.print_obj.id,
        'print_name': c.print_obj.name,
        'print_image': c.print_obj.image_url
    } for c in compat]
    return jsonify(result)

@catalog_bp.route('/get_stock', methods=['POST'])
def get_stock():
    """Возвращает остаток (stock) для выбранной комбинации."""
    model_id = request.form.get('model_id')
    color_id = request.form.get('color_id')
    size_id = request.form.get('size_id')

    combination = TShirtCombination.query.filter_by(
        model_id=model_id,
        color_id=color_id,
        size_id=size_id
    ).first()

    if combination:
        return jsonify({'stock': combination.stock})
    else:
        return jsonify({'stock': 0})

@catalog_bp.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    # Получаем параметры из запроса
    combination_id = request.form.get('combination_id')
    print_id = request.form.get('print_id', '0')
    final_print_id = print_id if print_id != '0' else None

    if 'cart' not in session:
        session['cart'] = []

    # Ищем элемент в корзине и уменьшаем его количество
    for i, item in enumerate(session['cart']):
        if item.get('combination_id') == int(combination_id) and item.get('print_id') == (final_print_id if final_print_id is None else int(final_print_id)):
            item['quantity'] -= 1
            # Если количество становится 0 или меньше, удаляем элемент
            if item['quantity'] <= 0:
                session['cart'].pop(i)
            break
    session.modified = True
    return jsonify({'success': True, 'cart': session['cart']})

@catalog_bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'cart' not in session:
        session['cart'] = []

    model_id = request.form.get('model_id')
    color_id = request.form.get('color_id')
    size_id = request.form.get('size_id')
    print_id = request.form.get('print_id', '0')  # '0' означает "без принта"
    quantity = int(request.form.get('quantity', 1))

    # Находим выбранную комбинацию (модель, цвет, размер)
    combination = TShirtCombination.query.filter_by(
        model_id=model_id,
        color_id=color_id,
        size_id=size_id
    ).first()

    if not combination:
        return "Данное сочетание не найдено или недоступно.", 400

    # Если выбран новый товар, проверяем, сколько уже добавлено для этой комбинации с выбранным принтом
    final_print_id = print_id if print_id != '0' else None
    existing_quantity = 0
    for item in session['cart']:
        if item.get('combination_id') == combination.id and item.get('print_id') == final_print_id:
            existing_quantity += item.get('quantity', 0)
    total_requested = existing_quantity + quantity
    if total_requested > combination.stock:
        return "Недостаточно товара на складе.", 400

    # Если выбран принт, проверяем его совместимость
    print_name = ""
    print_image = ""
    if final_print_id is not None:
        compatibility = PrintCompatibility.query.filter_by(
            combination_id=combination.id,
            print_id=final_print_id
        ).first()
        if not compatibility:
            return "Выбранный принт не сочетается с данной футболкой.", 400
        print_name = compatibility.print_obj.name
        print_image = compatibility.print_obj.image_url

    # Если товар с такой конфигурацией уже есть в корзине, увеличиваем количество, иначе добавляем новую запись
    found = False
    for item in session['cart']:
        if item.get('combination_id') == combination.id and item.get('print_id') == final_print_id:
            item['quantity'] += quantity
            found = True
            break

    if not found:
        cart_item = {
            'combination_id': combination.id,
            'model_name': combination.model.name,
            'color_name': combination.color.name,
            'size_name': combination.size.name,
            'print_id': final_print_id,
            'print_name': print_name,
            'quantity': quantity,
            'price': combination.model.price,
            'image_url': combination.combination_image,
            'print_image': print_image,
            'availableStock': combination.stock  # Сохраняем начальный остаток для отображения (опционально)
        }
        session['cart'].append(cart_item)

    session.modified = True
    return redirect(url_for('catalog.catalog'))

    if 'cart' not in session:
        session['cart'] = []

    model_id = request.form.get('model_id')
    color_id = request.form.get('color_id')
    size_id = request.form.get('size_id')
    print_id = request.form.get('print_id', '0')  # '0' означает "без принта"
    quantity = int(request.form.get('quantity', 1))

    combination = TShirtCombination.query.filter_by(
        model_id=model_id,
        color_id=color_id,
        size_id=size_id
    ).first()

    if not combination:
        return "Данное сочетание не найдено или недоступно.", 400

    if combination.stock < quantity:
        return "Недостаточно товара на складе.", 400

    # Если выбран принт, проверяем его совместимость
    print_name = ""
    print_image = ""
    if print_id != '0':
        compatibility = PrintCompatibility.query.filter_by(
            combination_id=combination.id,
            print_id=print_id
        ).first()
        if not compatibility:
            return "Выбранный принт не сочетается с данной футболкой.", 400
        print_name = compatibility.print_obj.name
        print_image = compatibility.print_obj.image_url

    # Если принт не выбран, используем None
    final_print_id = print_id if print_id != '0' else None

    # Проверяем, существует ли уже в корзине товар с такой же комбинацией и принтом
    found = False
    for item in session['cart']:
        if item.get('combination_id') == combination.id and item.get('print_id') == final_print_id:
            item['quantity'] += quantity
            found = True
            break

    if not found:
        cart_item = {
            'combination_id': combination.id,
            'model_name': combination.model.name,
            'color_name': combination.color.name,
            'size_name': combination.size.name,
            'print_id': final_print_id,
            'print_name': print_name,
            'quantity': quantity,
            'price': combination.model.price,
            'image_url': combination.combination_image,
            'print_image': print_image
        }
        session['cart'].append(cart_item)
    session.modified = True

    return redirect(url_for('catalog.catalog'))
