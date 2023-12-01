#### Триал-версия диплома для шпоры Диплом Путь Дао

Здесь реализован минимальный набор api, для того, чтобы загрузился фронт.
Также рабочие образцы тестов для CRUD api.
И самое вкусное конфиги для разворачивания в контейнерах.

Этого достаточно для резвого старта.


#### Запуск проекта
Клонируем код
git clone git@github.com:DEsipov/webinar_diplom_1.git

Собираем контейнеры
docker compose up –build

Заходим внутрь контейнера backend
docker exec -it infra-backend-1 bash

делаем миграции
./manage.py migrate

собираем статику
./manage.py collectstatic

создаем суперюзера.
./manage.py createsuperuser

Запускаем на localhost
проверяем работу, статики, медиа, админки, api.



### Полезные ссылки

Шпора
https://docs.google.com/document/d/132BqRgVzwE7qtLsO_A8PQBrs6XUf6ZZCr4SqT0Jgj3U/edit

