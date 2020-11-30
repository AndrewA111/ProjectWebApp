## Web-app for MSc Project

Coding challenge web-application that allows users to submit solutions to coding problems in Java via the in-page editor.

Application also allows priviledged users to upload new questions via an editor in the application.

## Setup

### Pre-requisites
Before running this web-application, the web-serivce used to compile user code must be running (see [CompilerAPI](https://github.com/AndrewA111/CompilerAPI)).

The address of this web-service must be included at the top of `/question/views.py`, as the variable `API_URL`.

This application has been developed using Python version 3.7.5.

### Running the application
It is recommended that this application is run in a virtual environment. Within your virtual environment, navigate to the project root directory and enter the following command to install dependencies:

`pip install -r requirements.txt` 

Still in the project root directory, type the following commands:

`python manage.py makemigrations`<br>
`python manage.py migrate`<br>
`python population_script.py`<br>
`python manage.py runserver`

The console output should provide the address where the website can be accessed.

