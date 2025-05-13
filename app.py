from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, current_user
from database import db_session, init_db
from models.user import User
from models.notification import Notification
import routes
import os
from datetime import datetime

app = Flask(__name__)
app.config.from_object('config.Config')

# Initialisation de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Enregistrement des blueprints
app.register_blueprint(routes.auth_bp)
app.register_blueprint(routes.home_bp)
app.register_blueprint(routes.dashboard_bp)
app.register_blueprint(routes.products_bp)
app.register_blueprint(routes.sales_bp)
app.register_blueprint(routes.clients_bp)
app.register_blueprint(routes.boutique_bp)
app.register_blueprint(routes.finances_bp)
app.register_blueprint(routes.commandes_bp)
app.register_blueprint(routes.factures_bp)
app.register_blueprint(routes.stock_bp)

# Context processor pour les notifications et la date actuelle
@app.context_processor
def inject_globals():
    notifications = []
    if current_user.is_authenticated:
        notifications = Notification.query.filter_by(is_read=False).order_by(Notification.created_at.desc()).limit(5).all()
    return dict(notifications=notifications, now=datetime.now())

@app.route('/')
def index():
    return redirect(url_for('home.index'))

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
