Deploy на Heroku
---------------------------------------------------------------------
Добавить в requirements.txt:
    psycopg2==<version>
    django-heroku==<version>
    gunicorn==<version>
    whitenoise==<version>
    dj-database-url==<version>

    - или установить их и pip freeze > requirements.txt:
        pip install psycopg2
        pip install django-heroku
        pip install gunicorn
        pip install whitenoise
        pip install dj-database-url
---------------------------------------------------------------------
Файлы Procfile и runtime.txt скопировать в корень проекта
    - в файле runtime.txt - актуальная версия Python (python-3.9.1)
    - в файле Procfile - (web: gunicorn config.wsgi --log-file -)
---------------------------------------------------------------------
В файле setting.py добавить в конец:

import dj_database_url
db_from_env = dj_database_url.config()
DATABASES["default"].update(db_from_env)

import django_heroku
django_heroku.settings(locals())
---------------------------------------------------------------------
В файле wsgi.py добавить в конец:

from whitenoise import WhiteNoise
application = WhiteNoise(application)
---------------------------------------------------------------------
