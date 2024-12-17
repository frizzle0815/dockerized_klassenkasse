from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.models import db, Participant, User, Collection
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)

@main.route('/')
def home():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin.view_collections'))
        elif current_user.is_organizer:
            return redirect(url_for('main.organizer_dashboard'))
    return redirect(url_for('main.public_view'))

@main.route('/setup', methods=['GET', 'POST'])
def setup():
    if User.query.filter_by(is_admin=True).first():
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email and password:
            hashed_password = generate_password_hash(password)
            admin = User(email=email, password=hashed_password, is_admin=True)
            db.session.add(admin)
            db.session.commit()
            flash('Admin account created. Please log in.', 'success')
            return redirect(url_for('main.login'))

        flash('Email and password are required.', 'danger')

    return render_template('setup.html')

@main.route('/public')
def public_view():
    collections = Collection.query.filter_by(is_active=True).all()
    return render_template('public_view.html', collections=collections)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('main.public_view'))

@main.route('/organizer')
@login_required
def organizer_dashboard():
    if not current_user.is_organizer:
        flash('Access unauthorized.', 'danger')
        return redirect(url_for('home'))

    collections = Collection.query.filter_by(organizer_id=current_user.id).all()
    return render_template('organizer_dashboard.html', collections=collections)

@main.route('/collection/<int:collection_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_collection(collection_id):
    collection = Collection.query.get_or_404(collection_id)

    if request.method == 'POST':
        collection.name = request.form.get('name')
        db.session.commit()
        flash('Collection updated successfully.', 'success')
        return redirect(url_for('main.organizer_dashboard'))

    return render_template('edit_collection.html', collection=collection)
    