FROM python:3.8.5

# Надо исправить: Сразу делаем WORKDIR, он создаст папку если ее нет и дальше можно не прописывать полный путь
WORKDIR /code

# Можно лучше: Копируем все сразу
COPY ./requirements.txt ./requirements.txt

# Надо исправить: Нигде не прописываем полный путь, тк мы уже сделали WORKDIR
RUN pip install -r requirements.txt

# Надо исправить: Оставляем CMD тут как требуют тесты, а из docker-compose убираем
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
