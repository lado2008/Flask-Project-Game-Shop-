from extensions import db, app, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
class BasceModel:
    def create(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def save(self):
        db.session.commit()

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    description = db.Column(db.String)
    img = db.Column(db.String)
    game = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='products')
    is_displayed = db.Column(db.Boolean, default=False)


class User(db.Model, BasceModel, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)
    products = db.relationship('Products', back_populates='user')

    def __init__(self, username, password, role):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role
    def check_password(self, password):
        return check_password_hash(self.password, password)

@login_manager.user_loader
def load_user(User_id):
    return User.query.get(User_id)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        admin_user = User(username="admin_user", password="password", role="admin")
        admin_user.create()
        normal_user = User(username="normal_user", password="password", role="guest")
        normal_user.create()