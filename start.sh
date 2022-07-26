python3 -m virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
export FLASK_APP=utils
export FLASK_DEBUG=0
export FLASK_ENV=production
flask run -h localhost -p 8000
