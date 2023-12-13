# Spending Tracker

Track your expenses and manage your budget effortlessly with Spending Tracker, a Python program powered by Flask and PostgreSQL.

## Technologies

- Python 3
- PostgreSQL

## Dependencies

Make sure to install the following dependencies:

```bash
pip3 install flask flask-sqlalchemy python-dotenv flask-migrate psycopg2
```

Create the PostgreSQL database:
```bash
createdb spending_tracker
```
In app.py, set the database URI:
```bash
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://<your postgres user>@localhost:5432/spending_tracker"
```

## How to run

Initialize and upgrade the database:
```bash
flask db init
flask db upgrade
```

Run the program:
```bash
python3 app.py
```

<!-- you should add a readme, it should contain the following -->
<!-- 1. context to the program, what is this, when did you do it, what are the technoglies used/what is needed to run the app-->
<!-- 2. some screen shots of the app, even better a youtube video, even even better host it online but that's like a whole project of it's own -->
<!-- 3. a _STEP_ by _STEP_ guide on how to get the app running-->
<!-- 4. add a seed  file so if someone wants to checkout your app they have some data to work with-->
