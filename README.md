# Task for Junior Fullstack Developer

Hi! I'm Michał and this is my code for Contact management page.
In my opinion, this code is not fully finished - I would like to add some statistics and exporting to csv.
I know that .env file should not be commited but for purpose of task I allowed myself commiting it.
## How to run the application

 1. Install [Docker](https://docs.docker.com/desktop/) (I have used Docker Desktop).
 2. Clone my code.
 3. Run docker-compose.yml which is located in main folder.
 4. After this you should be able to visit this [page](localhost:8080) for Contact management or [this](http://localhost:8080/admin/) for Admin page.
 5. To log in to the admin panel, use the username 'ADMIN' and the password '0YcoB0LIGE<v!ElQ3_&T'. This information is also in the .env file. Once logged in, you can create a user who can log in to the contact page.
 6. After Contact management page loads, clicking *Contacts* in upper left corner should redirect to the login page.

## What have I used?
I used:

 - Django as a backend and user authentication 
 - Svelte as a frontend | Used with DaisyUI and tailwindcss for page look and uppy for file upload
 - nginx as a proxy and load balancer
 - PostgreSql as a database for Django
 - docker for application containerization

## Backend - Django

When container is being made some informations are taken from .env file. I know it should not be included in Git but without it you would be able to run the app.

User can connect to the Django container using: *localhost:8080/api/* (nginx is handling that)
I have made two Django applications, first one for home/login page and second one for contact page. 
Login page is very simple, contains two inputs for login and password.
Contact page is technically much more complicated but I hope that for user it is easy to read and use.
Views where user makes request are protected by *@login_required* annotation and if user is not logged in, user gets redirected.

I have created 3 models:

 1. ContactStatusChoices which has only two fields - *id* and *name*. Those statuses are added to database while data migrating
 2. CityLocationWeather which has 7 fields - *name*, *latitude*, *longitude*, *temperature*, *humidity*, *wind_speed*, 				*last_updated* - primary key of this model is "name"
 3. Contact which has 9 fields - *id*, *name*, *surname*, *phone*, *email*, *city*, *status*, *add_date* and *user_id* - *city* and *status* are Foreign keys

## Frontend - Svelte

So frontend is not my strongest thing but I have tried to make it reliable and user friendly.
The connection to the frontend is also handled by nginx and can be connected using *localhost:8080/*.
There are 3 pages:

 1. Home page - right now it is empty but in future there will be something
 2. Login page
 3. Contact page - Containing user contacts. It allows to upload contact from .csv file, sort contacts and add contacts by hand. If contact is present it can be edited or deleted.

I hope it is responsive - I have tested but bugs might appear on other browsers 