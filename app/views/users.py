from flask import Blueprint, request, jsonify, redirect, render_template, url_for
from werkzeug.security import generate_password_hash

from app import db
from app.models import User, UserImage
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_user, logout_user, current_user
from flask import Flask, flash, redirect, render_template, \
     request, url_for
from app.forms import LoginForm, SignupForm

user_blueprint = Blueprint('user_blueprint', __name__)

@user_blueprint.route('/user/<int:user_id>/images', methods=['GET'])
def get_user_images(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    image_urls = [image.image_url for image in user.images.all()]
    return jsonify({'user_id': user_id, 'images': image_urls})


@user_blueprint.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return jsonify([user.to_dict() for user in users]), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

@user_blueprint.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        if user:
            return jsonify(user.to_dict()), 200
        return jsonify({"message": "User not found"}), 404
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

@user_blueprint.route('/user', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(
        voter_id=data.get('voter_id'),
        name=data.get('name'),
        email=data.get('email'),
        constituency=data.get('constituency')
    )
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

@user_blueprint.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.json
    try:
        user.voter_id = data.get('voter_id', user.voter_id)
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.constituency = data.get('constituency', user.constituency)
        db.session.commit()
        return jsonify(user.to_dict()), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

@user_blueprint.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted"}), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_blueprint.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard_blueprint.dashboard'))

        else:
            flash('Invalid email or password')
    return render_template('login.html', form = form)


@user_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(
            voter_id=form.voter_id.data,
            name=form.name.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            constituency=form.constituency.data
        )
        db.session.add(user)
        db.session.commit()
        # Redirect to a different page, e.g., login
        return redirect(url_for(user_blueprint.login))
    return render_template('signup.html', form=form)


@user_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('user_blueprint.login'))
