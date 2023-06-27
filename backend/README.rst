django app
==========

Usage
-----

.. code-block:: console

   git clone https://github.com/MartellOnell/djangoRestApp.git
   python -m venv django venv
   .\venv\Scripts\activate
   cd djangoRestApp
   pip install -r requirements.txt
   python manage.py makemigrations car
   python manage.py makemigrations authc
   python manage.py migrate
   python manage.py runserver
