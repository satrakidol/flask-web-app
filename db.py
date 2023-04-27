import oracledb
import os


def start_pool():

    # Generally a fixed-size pool is recommended, i.e. pool_min=pool_max.
    # Here the pool contains 4 connections, which is fine for 4 conncurrent
    # users and absolutely adequate for this demo.

    pool_min = 4
    pool_max = 4
    pool_inc = 0

    print("Connecting to", os.environ.get("DB_DSN"))
    print("Username ", os.environ.get("DB_USERNAME"))

    pool = oracledb.create_pool(
        user=os.environ.get("DB_USERNAME"),
        password=os.environ.get("DB_PASSWORD"),
        dsn=os.environ.get("DB_DSN"),
        min=pool_min,
        max=pool_max,
        increment=pool_inc
    )

    return pool


pool = start_pool()




def get_employees_with_department():
    with pool.acquire() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    "select A.ssn, A.fname, A.lname, A.salary, B.dname from employee A inner join department B on A.dno = B.dnumber")
                res = cursor.fetchall()
                employees = []
                for row in res:
                    print(row)
                    employees.append(
                        {'ssn': row[0],'name': row[1], 'surname': row[2], 'salary': row[3], 'department': row[4]})
                print(employees)

                return employees

            except oracledb.Error as err:
                error_obj, = err.args
                print(f"Error fetching Employees: {error_obj.message}")


def save_employee(ssn:int, firstname: str, lastname: str, salary:int, dep_id: int):
    with pool.acquire() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    "insert into employee (ssn, fname, lname, salary, dno) values (:ssn, :firstname, :lastname, :salary, :depid)", (ssn, firstname, lastname, salary, dep_id))
                connection.commit()
                return True
            except oracledb.Error as err:
                error_obj, = err.args
                print(f"Error saving employee: {error_obj.message}")



def get_employee(ssn: int):
    with pool.acquire() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    "select * from employee where ssn = :ssn", ssn=ssn)
                res = cursor.fetchone()
                print(res)
                employee = {'ssn': res[3], 'name': res[0], 'surname': res[2], 'salary': res[7], 'department': res[9]}
                print('fetched employee '.format(employee))
                return employee

            except oracledb.Error as err:
                error_obj, = err.args
                print(f"Error searching for Employee: {error_obj.message}")
                return False


def update_employee(ssn: int, firstname: str, lastname: str, salary: int, dep_id: int):
    with pool.acquire() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    "update employee set ssn = :ssn, fname = :firstname, lname = :lastname, salary = :salary, dno = :depid where ssn=:ssn", ssn=ssn, firstname=firstname, lastname=lastname, salary=salary, depid=dep_id)
                connection.commit()
                return True
            except oracledb.Error as err:
                error_obj, = err.args
                print(f"Error editing employee: {error_obj.message}")


def delete_employee(ssn: int):
    with pool.acquire() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    "delete from employee where ssn = :ssn", ssn=ssn)
                connection.commit()
                print('Employee {} deleted'.format(ssn))
                return True

            except oracledb.Error as err:
                error_obj, = err.args
                print(f"Error deleting Employee: {error_obj.message}")
                return False


def search_employees(lname: str):
    with pool.acquire() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    "select * from employee where lname = :lastname", lastname=lname)
                res = cursor.fetchall()
                employees = []
                for row in res:
                    print(row)
                    employees.append(
                        {'ssn': row[3], 'name': row[0], 'surname': row[2], 'salary': row[7], 'department': row[9]})
                print(employees)

                return employees

            except oracledb.Error as err:
                error_obj, = err.args
                print(f"Error searching for Employee: {error_obj.message}")


def get_departments():
    with pool.acquire() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    "select * from department")
                res = cursor.fetchall()
                departments = []
                for row in res:
                    print(row)
                    departments.append(
                        {'name': row[0], 'number': row[1], 'mgrssn': row[2], 'mgrstartdate': row[3]})
                print(departments)

                return departments

            except oracledb.Error as err:
                error_obj, = err.args
                print(f"Error fetching Departments: {error_obj.message}")



def get_projects_with_departments():
    with pool.acquire() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    "select A.pname, A.pnumber, A.plocation, B.dname from project A inner join department B on A.dnum = B.dnumber")
                res = cursor.fetchall()
                projects = []
                for row in res:
                    print(row)
                    projects.append(
                        {'name': row[0], 'number': row[1], 'location': row[2], 'department': row[3]})
                print(projects)

                return projects

            except oracledb.Error as err:
                error_obj, = err.args
                print(f"Error fetching Projects: {error_obj.message}")




def save_project(proname: str, pronumber: int, prolocation: str, depnum:int):
    with pool.acquire() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    "insert into project (pname, pnumber, plocation, dnum) values (:proname, :pronumber, :prolocation, :depnum)", (proname, pronumber, prolocation, depnum))
                connection.commit()
                return True
            except oracledb.Error as err:
                error_obj, = err.args
                print(f"Error saving project: {error_obj.message}")



def get_project(pnumber: int):
    with pool.acquire() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    "select * from project where pnumber = :pnumber", pnumber=pnumber)
                res = cursor.fetchone()
                print(res)
                project = {'name': res[0], 'number': res[1], 'location': res[2], 'department': res[3]}
                print('fetched project '.format(project))
                return project

            except oracledb.Error as err:
                error_obj, = err.args
                print(f"Error searching for project: {error_obj.message}")
                return False




def update_project(pname: str, pnumber: int, plocation: str, dnum: int):
    with pool.acquire() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    "update project set pname = :pname, pnumber = :pnumber, plocation = :plocation, dnum = :dnum where pnumber = :pnumber", pname=pname, pnumber=pnumber, plocation=plocation, dnum=dnum)
                connection.commit()
                return True
            except oracledb.Error as err:
                error_obj, = err.args
                print(f"Error editing project: {error_obj.message}")



def delete_project(pnumber: int):
    with pool.acquire() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    "delete from project where pnumber = :pnumber", pnumber=pnumber)
                connection.commit()
                print('Project {} deleted'.format(pnumber))
                return True

            except oracledb.Error as err:
                error_obj, = err.args
                print(f"Error deleting project: {error_obj.message}")
                return False



def get_works_on():
    with pool.acquire() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    "select C.lname, B.pname, A.hours from works_on A inner join project B on A.pno = B.pnumber inner join employee C on A.essn = C.ssn")
                res = cursor.fetchall()
                works_on = []
                for row in res:
                    print(row)
                    works_on.append(
                        {'name': row[0],'project': row[1], 'hours': row[2]})
                print(works_on)

                return works_on

            except oracledb.Error as err:
                error_obj, = err.args
                print(f"Error fetching Employees: {error_obj.message}")



def get_ssn(last_name: str):
    with pool.acquire() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    "select ssn from employee where lname = :lastname", lastname=last_name)
                res = cursor.fetchone()
                a=bool(res)
                if a==False:
                    res=['None',0]

                ssn = res[0]
                return ssn

            except oracledb.Error as err:
                error_obj, = err.args
                print(f"Error searching for project: {error_obj.message}")



def calculate_working_hours(ssn: int):
    with pool.acquire() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    "select hours from works_on where essn = :ssn", ssn=ssn)
                res = cursor.fetchall()
                hours = []
                for row in res:         
                    hours.append(row[0])

                total_hours=sum(hours)

                return total_hours

            except oracledb.Error as err:
                error_obj, = err.args
                print(f"Error calculating hours for Employee: {error_obj.message}")



def get_pnumber(projects:str):
    with pool.acquire() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    "select pnumber from project where pname = :projects", projects=projects)
                res = cursor.fetchone()
                a=bool(res)
                if a==False:
                    res=['None',0]

                pnumber = res[0]
        
                return pnumber

            except oracledb.Error as err:
                error_obj, = err.args
                print(f"Error searching for project number: {error_obj.message}")

def get_projects_essns(pnumber: int):
    with pool.acquire() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    "select A.essn, B.fname, B.lname from works_on A inner join employee B on A.essn = B.ssn where A.pno = :pnumber", pnumber=pnumber)
                res = cursor.fetchall()
                essns_employees = []
                for row in res:
                    essns_employees.append(
                        {'essn': row[0], 'fname': row[1], 'lname':row[2]})

                return essns_employees

            except oracledb.Error as err:
                error_obj, = err.args
                print(f"Error searching for essns: {error_obj.message}")