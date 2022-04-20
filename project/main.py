from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db
import pymysql.cursors

pymysql.install_as_MySQLdb()

connection = pymysql.connect(host='dpomserver.mysql.database.azure.com',
                             user='dpomserver@dpomserver',
                             password='#Freelance#123',
                             db='p1m',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@login_required
@main.route('/profile')
def profile():
    return render_template('profile.html', name=current_user.name, email=current_user.email)


@login_required
@main.route('/employee-dashboard')
def employee_dashboard():
    with connection.cursor() as cursor:
        data = cursor.execute("Select eid,name,reason,sdate,edate from employee ")
    if data > 0:
        row = cursor.fetchall()
    connection.commit()
    # cursor.close()
    return render_template('employee_dashboard.html', row=row)


@main.route('/leave-application')
def leave_application():
    return render_template('apply_form.html')


# admin
@login_required
@main.route('/admin-dashboard')
def admin_dashboard():
    with connection.cursor() as cursor:
        data = cursor.execute("Select * from employee ")
    if data > 0:
        row = cursor.fetchall()
    connection.commit()
    # cursor.close()
    return render_template('admin_dashboard.html.html', row=row)


@main.route('/vacation_applications')
def vacation_applications():
    return render_template('vacation_applications.html')


##################################################################################################################################################################################################################

# sql routes
@main.route('/holiday', methods=["POST", "GET"])
def book_tickets():
    return render_template('book_tickets.html')


@main.route('/apply', methods=["POST", "GET"])
def apply():
    name = request.form.get('name')
    eid = request.form.get('eid')
    reason = request.form.get('reason')
    sdate = request.form.get('date1')
    edate = request.form.get('date2')
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO employee(name,reason,sdate,edate) VALUES (%s,%s,%s,%s,%s) WHERE eid=(%s)",
                       (name, reason, sdate, edate,), (eid,))
        connection.commit()
    # cursor.close()
    return render_template('booked.html', bname=name, beid=eid, breason=reason, bdate=sdate, bedate=edate)


@main.route('/ifapprove', methods=["POST", "GET"])
def ifapprove():
    eid = request.form.get('eid')
    approve = request.form.get('approve')
    if approve == 1:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE employee SET approved=%s WHERE id=%s", (approve, eid,))
        connection.commit()

    return render_template('book_tickets.html')