from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@login_required
@main.route('/profile')
def profile():
    return render_template('profile.html', name=current_user.name, email=current_user.email)


@main.route('/employee-dashboard')
def employee_dashboard():
    return render_template('employee_dashboard.html')


@main.route('/leave-application')
def leave_application():
    return render_template('apply_form.html')


# admin
@main.route('/admin-dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')


@main.route('/vacation-applications')
def vacation_applications():
    return render_template('vacation_applications.html')


@main.route('/approved-applications')
def approved_applications():
    return render_template('approved_applications.html')