from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User, Collection, CollectionParticipant, Participant

main = Blueprint('main', __name__)

@main.route('/')
def public_collections():
    # Zeigt eine Übersicht aller aktiven Sammelaktionen
    active_collections = Collection.query.filter_by(is_active=True).all()
    return render_template('public_collections.html', collections=active_collections)

@main.route('/collection/<int:id>')
def collection_details(id):
    # Zeigt Details einer bestimmten Sammelaktion
    collection = Collection.query.get_or_404(id)
    participants = CollectionParticipant.query.filter_by(collection_id=id).all()
    return render_template('collection_details.html', collection=collection, participants=participants)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.organizer_dashboard' if user.is_organizer else 'admin.view_organizers'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('main.public_collections'))

@main.route('/organizer')
@login_required
def organizer_dashboard():
    # Zeigt Sammelaktionen des aktuellen Organisators an
    if not current_user.is_organizer:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('main.public_collections'))

    collections = Collection.query.filter_by(organizer_id=current_user.id).all()
    return render_template('organizer_dashboard.html', collections=collections)

@main.route('/collection/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def organizer_edit_collection(id):
    # Organisator kann nur seine eigenen Sammelaktionen bearbeiten
    collection = Collection.query.get_or_404(id)
    if collection.organizer_id != current_user.id:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('main.organizer_dashboard'))

    if request.method == 'POST':
        collection.name = request.form.get('name')
        db.session.commit()
        flash('Collection updated successfully.', 'success')
        return redirect(url_for('main.organizer_dashboard'))

    return render_template('edit_collection.html', collection=collection)
