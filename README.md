# To Do Backend

This Django backend serves as the backend for a to-do application. It provides RESTful API endpoints for managing tasks and users.

Link to front end repository: https://github.com/Aasmeen/to_do_frontend

## Prerequisites

- [Python](https://www.python.org/downloads/) (>=3.6)
- [Django](https://www.djangoproject.com/download/) (>=3.x)
- [Pip](https://pip.pypa.io/en/stable/installation/)
- [Pipenv](https://pypi.org/project/pipenv/)


## Set Up

1. Clone the project.
2. Navigate to the project directory and open the terminal. And run the following command

   `pipenv shell` to create a virtual environment.

   `pipenv install` to install required dependencies.
3. Install postgresql https://www.postgresql.org/download/
4. Create a new database using pgadmin.
5. Create settings_local.py file using settings_local.template file.
6. Run the server using the following command to check if everything is working fine.

   `python manage.py runserver`
7. Terminate the server and run the following command to apply the migrations.

    `python manage.py migrate`
8. Create a super user using the following command.

    `python manage.py createsuperuser`
9. Run the server using the following command.

    `python manage.py runserver` The API will be available at http://127.0.0.1:8000/.


## API Endpoints

### Authentication
&emsp; Login User: POST /api/login/

&emsp; Logout User: POST /api/logout/

&emsp; Register User: POST /api/register/

### Task
&emsp; User Basic Details: GET /api/base/

&emsp; List Tasks: GET /api/tasks/

&emsp; Create Task: POST /api/tasks/

&emsp; Retrieve Task: GET /api/tasks/<task_id>/

&emsp; Update Task: PATCH /api/tasks/<task_id>/

&emsp; Delete Task: DELETE /api/tasks/<task_id>/

## Authentication
User authentication is implemented using the Django REST framework's Token Authentication. To authenticate API requests, include the Authorization header with the format: Token YOUR_TOKEN.

## Run Test Cases
You can run the testcases using the following command:

`python manage.py tasks.test_views.py`

`python manage.py accounts.test_views.py`

