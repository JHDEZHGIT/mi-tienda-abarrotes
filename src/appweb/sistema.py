# src/appweb/sistema.py

from flask import Flask
from dotenv import load_dotenv
import os

from appweb.postgres_db import pgdb
from appweb.views import registrar_rutas

# ============================================
# CARGAR VARIABBLES .ENV
# ============================================

load_dotenv()

# ============================================
# OBTENER RUTAS ABSOLUTAS
# ============================================

# Directorio donde está este archivo (src/appweb)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Directorio de templates (src/templates)
TEMPLATE_DIR = os.path.join(BASE_DIR, '..', 'templates')

# Directorio de static (src/appweb/static) - donde está tu CSS actualmente
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# ============================================
# APP
# ============================================

app = Flask(__name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR,
    static_url_path='/static'
)

app.secret_key = os.getenv("SECRET_KEY")

# Configurar duración de sesión
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hora

# ============================================
# DB
# ============================================

pgdb.init_app(app)

# ============================================
# RUTAS
# ============================================

registrar_rutas(app)

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    print(f"BASE_DIR: {BASE_DIR}")
    print(f"TEMPLATE_DIR: {TEMPLATE_DIR}")
    print(f"STATIC_DIR: {STATIC_DIR}")
    app.run(debug=True)