django app
==========

Usage
-----
(предварительно установить docker и docker compose)
.. code-block:: console

   git clone https://github.com/MartellOnell/djangoRestApp.git
   cd djangoRestApp
   lsof -i :5432
   echo "если порт занят каким либо процессом, то смотрим его pid"
   kill <pid>
   sudo docker compose build
   sudo docker compose up
