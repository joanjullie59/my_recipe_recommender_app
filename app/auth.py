from flask import Blueprint, request, jsonify, flash, redirect, url_for, render_template
from flask_login import login_user, logout_user, login_required, current_user
from .models import db, User
from .routes import get_gemini_recipes

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
@login_required
def index():
    return render_template('index.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash('Invalid email or password')
            return redirect(url_for('auth.login'))
        login_user(user)
        next_page = request.args.get('next')
        return redirect(next_page or url_for('auth.index'))
    return render_template('login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address already exists. Please login instead.')
            return redirect(url_for('auth.signup'))
        new_user = User(email=email, username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please log in.')
        return redirect(url_for('auth.login'))
    return render_template('signup.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@auth_bp.route('/recipes', methods=['POST'])
def recipes():
    data = request.get_json()
    ingredients = data.get('ingredients', '')
    diet = data.get('diet', '')
    cuisine = data.get('cuisine', '')
    recipes = get_gemini_recipes(ingredients, diet, cuisine)
    return jsonify({'recipes': recipes})
