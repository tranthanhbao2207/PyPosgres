# PyPosgres
Python 2.7 - Flask

Pre:
 - py 2.7
 - PostgreSQL
 - Docker ( For postgresql server )
 - install https://virtualenvwrapper.readthedocs.io/en/latest/ and activate a virutalenv;
 - install python packages:
    pip install -r app/requirements


How to run :
 - 1. Run docker postgres:
    ./docker/postgres/start.sh
 - 2. Run init database (one time only):
    cd app;
    ./db.sh
 - 3. Run app:
    ./run.sh

Note: If files is not executable ,please execute this command :
    sudo chmod +x <file_path>


Usage:
 + Tools : Postman with body is raw and type = application/json
 + Routes:
    -  http://localhost:4100/zuser
        (method 'POST') : create new user
        (method 'GET' ) : get all user

    -  http://localhost:4100/zuser/<id>
        (method 'GET') : get an user
        (method 'PUT' ) : update an user

    -  http://localhost:4100/login2
        (method : POST ) : to login

    -  http://localhost:4100/logout2

    ## for CUSTOMER routes, login is required . If not login , they will return Unauthorized
    -  http://localhost:4100/customer
        (method 'POST') : create new customer
        (method 'GET' ) : get all customer

    -  http://localhost:4100/customer/<id>
        (method 'GET') : get an customer
        (method 'PUT' ) : update an customer

Note: for DELETE user/customer , we use PUT and attribute "deleted":True  in request body 



 
