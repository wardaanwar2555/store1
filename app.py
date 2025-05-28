from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # For flash messages and sessions
db_url=app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hello1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Define the User model
class Users(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Users {self.email}>'

# Create all tables
with app.app_context():
    db.create_all()
Base.metadata.create_all(engine)
# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        
        print("Received credentials:", email, password)

        # Check if user exists in the database
        user = session.query(Users).filter(Users.email == email).first()
        print("User fetched from DB:", user)

        if user:
            print("Stored password:", user.password)
            if user.password == password:
                print("Password matched.")
             #    session['user_email'] = email
              #  session['user_password'] = password  # ❌ Not secure in production
                return redirect(url_for('shop'))
            else:
                print("Password did not match.")
        else:
            print("User with email not found.")

        flash('Invalid email or password')

    return render_template('login.html')


# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            # Create and add user
            user = Users(email=email, password=password)
            session.add(user)
            session.commit()
            return render_template('login.html')
        except Exception as e:
            session.rollback()
        return render_template('signup.html')
            

    return render_template('signup.html')

# Other routes
@app.route('/platform')
def platform():
    return render_template('platform.html')

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/completeorder')
def completeorder():
    return render_template('completeorder.html')
@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/skin')
def skin():
    return render_template('skin.html')

@app.route('/hair')
def hair():
    return render_template('hair.html')

@app.route('/makeup')
def makeup():
    return render_template('makeup.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
