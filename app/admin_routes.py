from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db, User, Collection
from werkzeug.security import generate_password_hash

admin = Blueprint('admin', __name__)

@admin.before_request
def restrict_to_admins():
    if not current_user.is_authenticated or not current_user.is_admin:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('main.login'))

@admin.route('/admin/organizers')
def view_organizers():
    organizers = User.query.filter_by(is_organizer=True).all()
    return render_template('admin_organizers.html', organizers=organizers)

@admin.route('/admin/organizers/add', methods=['POST'])
def add_organizer():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        flash("Email and password are required.", "danger")
        return redirect(url_for('admin.view_organizers'))

    hashed_password = generate_password_hash(password)
    organizer = User(email=email, password=hashed_password, is_organizer=True)
    db.session.add(organizer)
    db.session.commit()

    flash("Organizer added successfully!", "success")
    return redirect(url_for('admin.view_organizers'))

@admin.route('/admin/collections')
def view_collections():
    collections = Collection.query.all()
    return render_template('admin_collections.html', collections=collections)

@admin.route('/admin/organizers/edit/<int:id>', methods=['POST'])
def edit_organizer(id):
    organizer = User.query.get(id)
    if organizer:
        email = request.form.get('email')
        password = request.form.get('password')

        if email:
            organizer.email = email
        if password:
            organizer.password = generate_password_hash(password)

        db.session.commit()
        flash("Organizer updated successfully!", "success")
    else:
        flash("Organizer not found.", "danger")

    return redirect(url_for('admin.view_organizers'))

@admin.route('/admin/collections/edit/<int:id>', methods=['POST'])
def edit_collection(id):
    collection = Collection.query.get(id)
    if collection:
        name = request.form.get('name')
        if name:
            collection.name = name
            db.session.commit()
            flash("Collection updated successfully!", "success")
    else:
        flash("Collection not found.", "danger")

    return redirect(url_for('admin.view_collections'))