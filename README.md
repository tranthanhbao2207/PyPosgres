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

Note: If files is not executable, please execute this command
    sudo chmod +x <file_path>


Usage:
 + Tools : Postman with body is raw and type = application/json
 + Routes:
    -  http://localhost:4100/zuser
        
        ( 'POST') : create new user
        
        ( 'GET' ) : get all user

    -  http://localhost:4100/zuser/<_id>
        
        ( 'GET') : get an user
        
        ( 'PUT' ) : update an user

    -  http://localhost:4100/login2
        
        ( 'POST' ) : to login

    -  http://localhost:4100/logout2

    -  http://localhost:4100/customer
        
        ( 'POST') : create new customer
        
        ( 'GET' ) : get all customer

    -  http://localhost:4100/customer/<_id>
        
        ( 'GET') : get an customer
        
        ( 'PUT' ) : update an customer

Note: 
- For CUSTOMER routes, login is required . If not login , they will return Unauthorized
- For DELETE user/customer , we use PUT and attribute "deleted":True  in request body 



Example:
 - Create user :
 https://2.pik.vn/2018e2721af1-1313-41bc-9227-1a5350437b09.png
 
 - Login: 
 https://2.pik.vn/20184ad41f13-3ff4-4180-ad7a-ba24c344f934.png
 
 - Edit Customer
 https://2.pik.vn/201814f2a51b-07f9-4d7c-af1d-c8c88c60e78a.png
