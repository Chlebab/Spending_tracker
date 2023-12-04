# Spending_tracker
This program allows a user to track spending and budget.
Written in Python.

Technologies: 
  -> Python3
  -> Postgresql

Dependencies:

Start guide:
  pip3 install flask
  pip3 install flask-sqlalchemy
  pip3 install python-dotenv
  pip3 install flask-migrate
  pip3 install psycopg2

  createdb spending_tracker

  in app.py
  app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://<your postgres user>@localhost:5432/spending_tracker"

Running the program:
  flask db init
  flask db upgrade



<!-- you should add a readme, it should contain the following -->
<!-- 1. context to the program, what is this, when did you do it, what are the technoglies used/what is needed to run the app-->
<!-- 2. some screen shots of the app, even better a youtube video, even even better host it online but that's like a whole project of it's own -->
<!-- 3. a _STEP_ by _STEP_ guide on how to get the app running-->
<!-- 4. add a seed  file so if someone wants to checkout your app they have some data to work with-->
