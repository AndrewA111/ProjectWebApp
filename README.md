## Web-app for MSc Project

Coding challenge web-application that allows users to submit solutions to coding problems in Java via the in-page editor.

Application also allows priviledged users to upload new questions via an editor in the application.

## Setup

### Pre-requisites
Before running this web-application, the web-serivce used to compile user code must be running (see CompilerAPI).

The address of this web-service must be included at the top of `/question/views.py`, as the variable `API_URL`.

### Running the application
Download the project then navigate to the project root directory and type the following commands:

>python manage.py makemigrations<br>
>python manage.py migrate<br>
>python population_script.py<br>
>python manage.py runserver

The console output should provide the address where the website can be accessed.

