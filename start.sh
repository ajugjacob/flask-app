source env/bin/activate
export FLASK_APP=run.py
export FLASK_DEBUG=1
export FLASK_ENV=development
flask run -h localhost -p 8000
