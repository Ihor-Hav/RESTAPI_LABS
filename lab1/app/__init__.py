from flask import Flask

app = Flask(__name__)

# Імпортуємо views після ініціалізації app
from app import views
