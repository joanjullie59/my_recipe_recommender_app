from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return render_template('index.html')

@main_bp.route('/recipes', methods=['GET', 'POST'])
@login_required
def recipes():
    # Recipe logic here
    return jsonify({"message": "Recipe endpoint"})

@main_bp.route('/history', methods=['GET'])
@login_required
def get_history():
    user_email = current_user.email
    history_data = [
        {"recipe": "Spaghetti Bolognese", "date": "2025-09-01"},
        {"recipe": "Vegan Tacos", "date": "2025-08-30"},
    ]
    return jsonify({"user": user_email, "history": history_data})
