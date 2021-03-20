# Stocks App

This is a Django app that lets you buy and sell stocks on the NASDAQ with a virtual portfolio. See how you do against others via the leaderboard.

HOST: https://stock-portfolio-ndp96.ondigitalocean.app

This app uses the IEX Cloud API to fill in the varying stock information. However, the key I'm using is for the sandbox mode, so the numbers are not accurate to real market prices!

## Getting Started

This app was written with Django 3.1.2. Additional plugins/requirements are in requirements.txt.

I recommend using python's **virtualenv** tool if building locally:

> $ mkvirtualenv *django_env*
> $ python manage.py runserver

Then visit http://localhost:8000 in your web browser to view the app. 

### Settings

This app has two different settings; one for development and one for production. You'll have to change two things: the DATABASES and the API key. The current settings are set for production.

In development, set the DATABASE in shared_settings.py to:

> DATABASES = {
>     'default': {
>         'ENGINE': 'django.db.backends.sqlite3',
>         'NAME': BASE_DIR / 'db.sqlite3',
>     }
> }

You can comment out the other database settings in the file until you want to put the app back into production settings.

For the API key in production, create: **updated_stocks/updated_stocks/settings/private_settings.py**. In it, put your CLOUD_API_KEY. 

If in production, you should assign the API key and secret key to environmental variables. (ex. os.environ['SECRET_KEY'])

## Screenshots

![ss1](/screenshots/1.png?raw=true)
![ss2](/screenshots/2.png?raw=true)
![ss3](/screenshots/3.png?raw=true)