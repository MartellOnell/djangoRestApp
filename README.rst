django app
==========

Usage
-----
.. code-block:: console
   
   sudo git clone https://github.com/MartellOnell/djangoRestApp.git
   cd djangoRestApp
   sudo lsof -i :5432
   echo "если порт занят каким либо процессом, то смотрим его pid"
   sudo kill <pid>
   sudo ./start.sh
