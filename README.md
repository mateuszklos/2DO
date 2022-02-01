
 # //WRITING IN PROGRESS

# 2DO planner


link: https://salty-ocean-planner.herokuapp.com/

This is a CRUD application that allows users to manage their tasks.
It was made in Python 3.10 (Django 4.0.1)

Static frontend was made in Bootstrap Studio (available in Github Student Developer Pack)

## account creation

User should create account, setting username and password.
Otherwise, there is no access to the tasks management.
Registration form is available in /register page.


## login
Whether account exists, user can log into the planner using credentials
set in registration.
Login form is located in the landing page (index).
Being logged in is required to get access to the content, otherwise
2DO would display login form, and then redirect to desired page.

# tasks
Every user has their own tasks.
2DO prevents other users deleting, editing and completing another user's tasks.
Task attributes:
* title - string with max_length=50
* author - user who added a task
* creation_date - date field containing date of task creation
* is_completed  - boolean field with information if task is completed or not
* completed_at - date field with null if not completed, and with date of task completion if completed


## dashboard
/dashboard is a page where user is redirected straight after login. 
Here can be found user's active tasks. With clicking a 'plus +' icon next to the
'active tasks' heading, user can add own task. After that, task will be
visible underneath.



Tasks are paginated by 8 elements per page.
## archive
archive description

## searching

searching description

## statistics

statistics description

## export to .xls file
User can export the data sheet containing both finished and not finished tasks.

## REST Api view
rest api description
