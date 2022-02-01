# 2DO planner


link: https://salty-ocean-planner.herokuapp.com/

This is a CRUD application that allows users to manage their tasks.
It was made in Python 3.10 (Django 4.0.1)

Static frontend was made in Bootstrap Studio (available in Github Student Developer Pack). 2DO is fully responsive on widely used screen resolutions.

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
User is logged out automatically after 600 secs.

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
In card with task information are located three icons - completing task, editing task's title, and deleting task.
The latter removing selected task straight from database and it's premanent operation.
Editing task allows user to change it's title. Completing task moving it to the archive.

Tasks are paginated by 8 elements per page.
## archive
/archive is a place where completed tasks are stored. The page view is identical to the /dashboard. 
User also can delete completed task, but cannot edit.
Tasks in archive contain date of completion.

Tasks are paginated by 8 elements per page.
## searching

Bot in /dashboard and /archive, there is located a search bar,
that allows users to search within their task's titles.


Found tasks are paginated by 8 elements per page.
## statistics

/statistic is the page, where use can see their's percentage tasks completion.
There are shown both finished and not finished tasks and it's amount.
By clicking an icon with Excel file, there is a possibility to generate .xlsx file.


## export to .xls file
User can export the data sheet containing both finished and not finished tasks.
By clicking Excel icon, there will automatically appear the file explorer with a place to save the file.
File contains all the tasks made by current user.
If task is completed, it will have TRUE (in Libre Office 1) set in column is_completed.
Otherwise, it will have FALSE value (0).

## REST Api view
USing Django REST Framework, 2DO allows users to connect with another application with REST API.

