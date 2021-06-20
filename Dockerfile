# стащить Python 3 с докерхаба
FROM python:3

# создать рабочую дерикторию
WORKDIR /usr/src/app

# копировать requirements.txt и entrypoint.sh в рабочую дерикторию
COPY requirements.txt .
COPY entrypoint.sh .

# запуск команды для установки необходимых пакетов
RUN pip install -r requirements.txt
# сделать исполняемым файл entrypoint.sh
RUN chmod +x entrypoint.sh

# копировать все в рабочую дерикторию
COPY . .

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
