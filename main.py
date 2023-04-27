from flask import Flask, redirect, url_for, request, render_template
from flask_bootstrap import Bootstrap

import os
from dotenv import load_dotenv

from db import search_employees, get_departments, save_employee, get_projects_with_departments, get_employees_with_department, save_project, delete_employee, get_employee, update_employee, get_project, update_project, delete_project, get_works_on, calculate_working_hours, get_ssn, get_pnumber, get_projects_essns


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    print('APP_NAME is {}'.format(os.environ.get('APP_NAME')))
else:
    raise RuntimeError('Not found application configuration')



app = Flask(__name__)
Bootstrap(app)

app.logger.info('Environmental variables Initialized')




@app.route('/')
def home():
    return render_template('base.html')


@app.route('/employees')
def show_employees():
    employees = get_employees_with_department()
    return render_template('employees.html', employees=employees)



@app.route('/employees/save', methods=['GET', 'POST'])
def show_employee_form():
    if request.method == 'POST':
        ssn = request.form['ssn']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        salary = request.form['salary']
        department_id = request.form['department_id']
        print('ssn {} - first name {} - last name {} - salary - {} - dep id - {}'.format(ssn, first_name, last_name, salary, department_id))
        save_employee(ssn=ssn, firstname=first_name, lastname=last_name, salary=salary, dep_id=department_id)
        return redirect(url_for('show_employees'))
    else:
        depts = get_departments()
        return render_template('employee_form.html', departments=depts)


@app.route('/employees/edit/<int:emp_id>', methods=['GET', 'POST'])
def edit_employee(emp_id):
    if request.method == 'GET':
        emp = get_employee(emp_id)
        print('employee {}'.format(emp))
        depts = get_departments()
        return render_template('employee_form.html', departments=depts, employee=emp)
    if request.method == 'POST':
        if request.method == 'POST':
            ssn = request.form['ssn']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            salary = request.form['salary']
            department_id = request.form['department_id']
            print('ssn {} - first name {} - last name {} - salary - {} - dep id - {}'.format(
                ssn, first_name, last_name, salary, department_id))
            emp = get_employee(ssn)
            if emp:
                update_employee(ssn=ssn, firstname=first_name, lastname=last_name, salary=salary, dep_id=department_id)
            else:
                save_employee(ssn=ssn, firstname=first_name, lastname=last_name, salary=salary, dep_id=department_id)
            return redirect(url_for('show_employees'))

@app.route('/employees/delete/<int:emp_id>', methods=['POST'])
def del_employee(emp_id):
    result = delete_employee(emp_id)
    return redirect(url_for('show_employees'))


# # @app.route('/name', methods = ['POST', 'GET'])
# # def get_name():
# #     if request.method == 'POST':
# #         user = request.form['name']
# #         return redirect(url_for('say_hello', username = user))
# #     else:
# #         return render_template('user_form.html')





@app.route('/employees/search', methods = ['GET','POST'])
def display_search_employees():
    if request.method == 'POST':
        last_name = request.form['last_name']
        return redirect(url_for('search_lname_employees', lname = last_name))
    else:
        return render_template('search_employees.html')

@app.route('/employees/search/<string:lname>')
def search_lname_employees(lname):
    employees = search_employees(lname)
    print(employees)
    return render_template('employees.html', employees=employees)


@app.route('/projects')
def show_projects():
    projects = get_projects_with_departments()
    return render_template('projects.html', projects=projects)


@app.route('/projects/save', methods=['GET', 'POST'])
def show_project_form():
    if request.method == 'POST':
        pname = request.form['pname']
        pnumber = request.form['pnumber']
        plocation = request.form['plocation']
        dnum = request.form['dnum']
        print('name {} - number - {} - location - {} - department - {}'.format(pname, pnumber, plocation, dnum))
        save_project(proname=pname, pronumber=pnumber, prolocation=plocation, depnum=dnum)
        return redirect(url_for('show_projects'))
    else:
        depts = get_departments()
        return render_template('project_form.html', departments=depts)

@app.route('/projects/edit/<int:pro_num>', methods=['GET', 'POST'])
def edit_project(pro_num):
    if request.method == 'GET':
        pro = get_project(pro_num)
        print('project {}'.format(pro))
        depts = get_departments()
        return render_template('project_form.html', departments=depts, project=pro)
    if request.method == 'POST':
        if request.method == 'POST':
            pname = request.form['pname']
            pnumber = request.form['pnumber']
            plocation = request.form['plocation']
            dnum = request.form['dnum']
            print('project_name {} - project_number {} - location {} - department {}'.format(
                pname, pnumber, plocation, dnum))
            pro = get_project(pnumber)
            if pro:
                update_project(pname=pname, pnumber=pnumber, plocation=plocation, dnum=dnum)
            else:
                save_project(proname=pname, pronumber=pnumber, prolocation=plocation, depnum=dnum)
            return redirect(url_for('show_projects'))



@app.route('/projects/delete/<int:pro_num>', methods=['POST'])
def del_project(pro_num):
    result = delete_project(pro_num)
    return redirect(url_for('show_projects'))



@app.route('/calculate_working_hours', methods = ['GET','POST'])
def show_search_employee():
    global last_name
    if request.method == 'POST':
        last_name = request.form['last_name']
        ssn = get_ssn(last_name)
        if ssn=='None':
            return render_template('cannot_find_employee.html')
        else:
            return redirect(url_for('show_total_working_hours', ssn=ssn))
    else:
        return render_template('search_employees.html')

@app.route('/calculate_working_hours/<int:ssn>')
def show_total_working_hours(ssn):
    total_hours = calculate_working_hours(ssn)
    print(total_hours)
    return render_template('total_hours.html', total_hours=total_hours, last_name=last_name)



@app.route('/Works_On', methods = ['GET','POST'])
def works_on():
    global projects
    if request.method == 'POST':
        projects = request.form['projects']
        pnumber=get_pnumber(projects)
        if pnumber=='None':
            return render_template('cannot_find_project.html')
        else:
            return redirect(url_for('search_projects_employees', pnumber = pnumber))
    else:
        works_on = get_works_on()
        return render_template('works_on.html', works_on=works_on)



@app.route('/Works_On/search/<int:pnumber>')
def search_projects_employees(pnumber):
    essns_employees = get_projects_essns(pnumber)
    print(essns_employees)
    return render_template('employees_working_on_project.html', essns_employees=essns_employees, projects=projects)