web: flask db upgrade; gunicorn task_list:'create_app()'
heroku config:set FLASK_APP=task_list
heroku config:set SECRET_KEY="`< /dev/urandom tr -dc 'a-zA-Z0-9' | head -c16`"