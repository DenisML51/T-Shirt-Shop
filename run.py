from flask import Flask, redirect, url_for, session
import config
from models.db import db
from controllers.catalog_controller import catalog_bp
from controllers.order_controller import order_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)

    app.register_blueprint(catalog_bp)
    app.register_blueprint(order_bp)

    @app.route('/')
    def index():
        return redirect(url_for('catalog.catalog'))

    @app.route('/cancel_all', methods=['GET'])
    def cancel_all():
        session.clear()  
        return redirect(url_for('catalog.catalog'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
