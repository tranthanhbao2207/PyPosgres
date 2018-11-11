#Pre
 - python 2.7 
 - Postgres 
 - installed https://virtualenvwrapper.readthedocs.io/en/latest/

#How to run
 - create virtualenv
 
 - install packages :
   pip install -r app/requirements
   
 - run migration (chmod +x <file> if allowed):
   ./db.sh
   
 - run app (chmod +x <file> if not allowed):
   ./run.sh
