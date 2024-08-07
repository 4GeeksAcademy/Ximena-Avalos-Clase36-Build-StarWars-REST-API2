import os
from flask_admin import Admin
from models import db, User, Planet, People, Vehicle
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='Star Wars API Admin', template_mode='bootstrap3')

    # Add administrative views here
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Planet, db.session))
    admin.add_view(ModelView(People, db.session))
    admin.add_view(ModelView(Vehicle, db.session))

# Additional admin configuration can be added here if necessary