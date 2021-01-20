# Blog Sparrow

A blog build with Django!

[![Build Status](https://travis-ci.com/nickolasaperes/blog-sparrow.svg?branch=master)](https://travis-ci.com/nickolasaperes/blog-sparrow)

## Quick Start

1. Clone the repo
2. Create a virtualenv with Python 3.7.
3. Activate the virtualenv.
4. Install the dependencies (psycopg2 is not necessary for development).
5. Configure the instance with the .env file
6. Generate a SECRET_KEY and paste in .env
7. Run the tests.

```console
git clone https://github.com/nickolasaperes/blog-sparrow.git sparrow
cd sparrow
python -m venv env
source env/bin/activate
pip install -r requirements.txt
cp contrib/env-sample .env
python contrib/secret_gen.py
python manage.py test
```

## How to deploy?

1. Create a heroku app.
2. Send the settings to the app.
3. Define a secure SECRET_KEY for the instance.
4. Define DEBUG=False
5. Push the code to heroku.

```console
heroku create minhainstancia
heroku config:push
heroku config:set SECRET_KEY=`python manage.py generate_secret_key`
heroku config:set DEBUG=False
git push heroku master --force
```

## Template

Thanks to [Styleshout](https://www.styleshout.com/) for the free template!