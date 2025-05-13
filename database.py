from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

engine = create_engine('sqlite:///inventobot.db')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # Import all modules here that define models
    from models.product import Product
    from models.sale import Sale
    from models.client import Client
    from models.user import User
    from models.notification import Notification
    Base.metadata.create_all(bind=engine)
    
    # Créer un utilisateur admin par défaut si aucun utilisateur n'existe
    from models.user import User
    if User.query.count() == 0:
        from werkzeug.security import generate_password_hash
        admin = User(username='admin', email='admin@inventobot.com', is_admin=True)
        admin.password_hash = generate_password_hash('admin')
        db_session.add(admin)
        db_session.commit()
