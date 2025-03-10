from flask import Flask
from models.db import db
from models.models import (
    TShirtModel, Color, Size, Print,
    TShirtCombination, PrintCompatibility
)
import config

def init_database():
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Создаем модели футболок
        model1 = TShirtModel(name="Classic Tee", base_image="static/images/classic_white.png", price=10.0)
        model2 = TShirtModel(name="V-Neck Tee", base_image="static/images/vneck_white.png", price=12.0)
        
        # Создаем цвета
        color_white = Color(name="White", hex_code="#FFFFFF")
        color_black = Color(name="Black", hex_code="#000000")
        color_red   = Color(name="Red", hex_code="#FF0000")
        color_blue  = Color(name="Blue", hex_code="#0000FF")
        
        # Создаем размеры
        size_s = Size(name="S")
        size_m = Size(name="M")
        size_l = Size(name="L")
        size_xl = Size(name="XL")
        
        # Создаем 7 принтов
        print1 = Print(name="Logo Print", image_url="static/prints/logo.png")
        print2 = Print(name="Funny Text", image_url="static/prints/funny_text.png")
        print3 = Print(name="Minimalist Art", image_url="static/prints/minimalist.png")
        print4 = Print(name="Abstract", image_url="static/prints/abstract.png")
        print5 = Print(name="Nature", image_url="static/prints/nature.png")
        print6 = Print(name="Geometric", image_url="static/prints/geometric.png")
        print7 = Print(name="Vintage Vibes", image_url="static/prints/vintage_vibes.png")
        
        db.session.add_all([
            model1, model2,
            color_white, color_black, color_red, color_blue,
            size_s, size_m, size_l, size_xl,
            print1, print2, print3, print4, print5, print6, print7
        ])
        db.session.commit()
        
        # Создаем товарные сочетания (для каждой модели и цвета создадим сочетания для всех размеров)
        # Для Classic Tee
        comb1 = TShirtCombination(model_id=model1.id, color_id=color_white.id, size_id=size_s.id, stock=10, combination_image="static/images/classic_white.png")
        comb2 = TShirtCombination(model_id=model1.id, color_id=color_white.id, size_id=size_m.id, stock=8, combination_image="static/images/classic_white.png")
        comb3 = TShirtCombination(model_id=model1.id, color_id=color_black.id, size_id=size_s.id, stock=5, combination_image="static/images/classic_black.png")
        comb4 = TShirtCombination(model_id=model1.id, color_id=color_red.id,   size_id=size_l.id, stock=8, combination_image="static/images/classic_red.png")
        comb5 = TShirtCombination(model_id=model1.id, color_id=color_blue.id,  size_id=size_s.id, stock=7, combination_image="static/images/classic_blue.png")
        
        # Для V-Neck Tee
        comb6 = TShirtCombination(model_id=model2.id, color_id=color_white.id, size_id=size_l.id, stock=7, combination_image="static/images/vneck_white.png")
        comb7 = TShirtCombination(model_id=model2.id, color_id=color_black.id, size_id=size_m.id, stock=9, combination_image="static/images/vneck_black.png")
        comb8 = TShirtCombination(model_id=model2.id, color_id=color_blue.id,  size_id=size_xl.id, stock=4, combination_image="static/images/vneck_blue.png")
        comb9 = TShirtCombination(model_id=model2.id, color_id=color_red.id,   size_id=size_m.id, stock=6, combination_image="static/images/vneck_red.png")
        
    
        
        db.session.add_all([comb1, comb2, comb3, comb4, comb5, comb6, comb7, comb8, comb9])
        db.session.commit()
        
        # Определяем набор принтов для каждой пары (Модель, Цвет)
        # Один и тот же набор применяется ко всем размерам выбранной модели и цвета.
        allowed_prints = {
            ("Classic Tee", "White"): [print1.id, print2.id, print3.id, print6.id],
            ("Classic Tee", "Black"): [print1.id, print4.id, print5.id],
            ("Classic Tee", "Red"):   [print2.id, print3.id, print6.id, print7.id],
            ("Classic Tee", "Blue"):  [print1.id, print2.id, print3.id, print4.id],
            ("V-Neck Tee", "White"):   [print3.id, print4.id, print5.id, print6.id],
            ("V-Neck Tee", "Black"):   [print1.id, print2.id, print7.id],
            ("V-Neck Tee", "Red"):     [print1.id, print3.id, print5.id, print7.id],
            ("V-Neck Tee", "Blue"):    [print2.id, print4.id, print6.id],
        }
        
        # Добавляем записи PrintCompatibility для каждой комбинации на основе (Модель, Цвет)
        all_combs = [comb1, comb2, comb3, comb4, comb5, comb6, comb7, comb8, comb9]
        for comb in all_combs:
            key = (comb.model.name, comb.color.name)
            if key in allowed_prints:
                for pid in allowed_prints[key]:
                    db.session.add(PrintCompatibility(combination_id=comb.id, print_id=pid))
        
        db.session.commit()
        print("Database initialized with extended data: 3 models, 4 colors, 4 sizes, 7 prints, and print sets based on model and color.")

if __name__ == '__main__':
    init_database()
