echo "Инициализация базы данных..."
python init_db.py

echo "Запуск приложения..."
exec gunicorn --bind 0.0.0.0:5000 app:create_app()
