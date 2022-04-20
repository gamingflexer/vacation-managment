from flask import Blueprint, render_template, request,redirect,url_for
from flask_login import login_required, current_user
from . import db
import pymysql.cursors
pymysql.install_as_MySQLdb()



connection = pymysql.connect(host='dpomserver.mysql.database.azure.com',
                             user='dpomserver@dpomserver',
                             password='#Freelance#123',
                             db='p2v',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/verify')
def verify():
    return render_template('verify.html')

@login_required
@main.route('/profile')
def profile():
    return render_template('profile.html', name="current_user.name", email="current_user.email")


@login_required
@main.route('/employee-dashboard')
def employee_dashboard():
    with connection.cursor() as cursor0:
        data = cursor0.execute("Select name,reason2,sdate,edate,approved from employee ")
    if data > 0:
        row = cursor0.fetchall()
    connection.commit()
    #cursor.close()
    return render_template('employee_dashboard.html',row=row)


# admin
@main.route('/admin-dashboard', methods=["POST", "GET"])
def admin_dashboard():
    return render_template('admin_dashboard.html')


@main.route('/vacation_applications', methods=["POST", "GET"])
def vacation_applications():
    try:
        with connection.cursor() as cursor:
            data = cursor.execute("SELECT * from employee WHERE approved='Pending' ")
        if data > 0:
            row = cursor.fetchall()
            connection.commit()
        else:
            row = []
    except Exception as e:
        row = []
        print("error" + e[10])
    # cursor.close()
    return render_template('vacation_applications.html',row=row)

@main.route('/approved-dashboard')
def approved_applications():
    with connection.cursor() as cursor:
        data = cursor.execute("SELECT * from employee WHERE approved='approved' ")
    if data > 0:
        row = cursor.fetchall()
    connection.commit()
    # cursor.close()
    return render_template('approved_applications.html',row=row)

@main.route('/leave-application', methods=["POST", "GET"])
def leave_application():
    return render_template('apply_form.html')


@main.route('/added', methods=["POST", "GET"])
def added():
    reason = request.form.get('reason')
    sdate = request.form.get('start_date')
    edate = request.form.get('end_date')
    eid = request.form.get('eid')
    
    print(reason,sdate,edate,eid)

    with connection.cursor() as cursor:
        cursor.execute("update employee set reason2=%s, sdate=%s, edate=%s ,approved='Pending' where eid=%s ",(reason,sdate,edate,eid,))
        connection.commit()
    return render_template('employee_dashboard.html')

@main.route('/accept/<int:eid>', methods=["POST", "GET"])
def approval(eid):
    approve = request.form.get('admin_response')
    with connection.cursor() as cursor:
        data = cursor.execute("UPDATE employee set approved = %s WHERE eid =%s",(approve,eid,))
    if data > 0:
        row = cursor.fetchall()
    connection.commit()
    return redirect(url_for('main.approved_applications'))

@main.route('/reject/<int:eid>', methods=["POST", "GET"])
def reject(eid):
    approve = request.form.get('admin_response')
    with connection.cursor() as cursor:
        data = cursor.execute("UPDATE employee set approved = %s WHERE eid =%s",(approve,eid,))
    if data > 0:
        row = cursor.fetchall()
    connection.commit()
    return redirect(url_for('main.approved_applications'))