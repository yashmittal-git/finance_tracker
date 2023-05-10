from app import app, db, login_manager
from config import Config

if __name__ == '__main__':
    app.config.from_object(Config)
    app.run(debug = True, host='0.0.0.0', port=5000)
