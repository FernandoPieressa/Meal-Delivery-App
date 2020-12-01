# Backend-Test-Pieressa

## Requirements

- Postgres: 10
- Python: 3.7

Python libraries needed can be found in requirements.txt

## Enviroment variables

To run the application, it will be necessary to provide the following envs:

- ENV_ROLE: Represents in what role the application will start (development/production)
- SLACK_TOKEN: Slack app token. The slack application must have permissions to send reminders
- DB_PASSWORD: password of the postgres user that holds the app database
- DB_USER: username of the postgres user that holds the app database

## How to initialize APP

To install all Django requirements run

```
pip install requirements.txt
```
### If you want to can create a virtual environment (Recommended, hygiene is good)

For Unix-like (MAC and Linux)

```
virtualenv -p python3.7 env
source env/bin/activate
```

For Windows
```
virtualenv -p python3.7 env
.env/Scripts/activate
```

## How to run APP

1. Create a postgres database with the name `backend_test_pieressa` and assign a psql user
2. Set up env variables as written above
3. `python manage.py migrate`
4. `python manage.py populate_db` (This is a custom made function, used to create the initial user that will manage the meal application, considering that you can't create a new user without being logged in for security reasons). The user will have name `administrator` and password `123456123a`
5. `python manage.py runserver`

### To run test

`python manage.py test`


## How to use the app

The users will need to authenticate to use most functionalities. The only function you can do without logging in is choose a specific meal if you are an employee. use the command `populate_db` to create an initial user.

Once a user has logged in, it will be possible to create new meals on the *Menu* tab, by specifying a day and meal names. The user will be able to add multiple meals in one form. If the user needs to edit the menu for a day, it will have to delete a meal and create it again by searching for it in the *Home* view

The *Home* view can filter and show the meals available given a specific date, and also show the food selection done by each employee. Once a date has been given, and only if there are any meals in the given date, the user can send slack reminders to every single employee on the system. Once the slack reminders has been sent, the a new table will appear with the food selection for a specific date. The employees will receive a notification *1 minute* after the slack reminder has been sent by the user.

The *Employees* tab can let the user add and delete Employees from the system. It's important to put as username the slack id of the employee to correctly receive the reminder.

The user can also register new admin users to manage the Meal Delivery app by using the *Register* tab.

After a reminder has been sent, employees will be able to click the link in the slack reminder with the format:

´´´
{protocol}://{host}/menu/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxxx
´´´

Where they can choose their meal and add specifications. This can only be done if its before 11:00am and at the the same day of the Menu, if not the Employee will receive a link expired message.

## Final Notes

- To make the publication of reminders asynchronous, and given that Django 3.0.5 was used, threading was used to create one running thread for each of the reminder to be sent.

- Thanks for your time!
