## V MESTE - сервис для поиска компании для настольных игр
https://v-meste.fun/

### Описание
Платформа для поиска компании для настольных игр: создание и поиск встреч по заданным фильтрам

### Используемые технологии:
![image](https://img.shields.io/badge/Python%203.9-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/Django%203.2-092E20?style=for-the-badge&logo=django&logoColor=green)
![image](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![image](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)
![image](https://img.shields.io/badge/</>%20HTMX-F00A00?style=for-the-badge&logo=htmx&logoColor=white)
![image](https://img.shields.io/badge/Chart%20js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)
![image](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![image](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![image](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
![image](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)
![image](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

### Доступные возможности
- Личный кабинет пользователя (расширенная модель);
- Загрузка данных о пользователе и коллекции игр с tesera.ru по API;
- Обновляемая по API база настольных игр;
- Создание встреч (место, дата, игры, кол-во игроков и т.д.);
- Поиск встреч по фильтрам (геолокация с радиусом поиска, дата, игра) с интерактивной картой;
- Запись партий (опционально: новых/на основании встреч/других партий) с htmx;
- Статистика партий с графиками Chart.js;
- Телеграм-бот, оповещающий об изменениях в играх пользователя и создании новых встреч по фильтру;

### Будущие обновления
Готова MVP версия и CI/CD для обновления проекта на сервере. Ближайшие обновления:
- Улучшенная навигация (боковая панель) - сделано;
- История партий в настольные игры и статистика по ним - сделано;
- Автотесты;
- Блок для клубов: закрытые встречи, расширенный кабинет;
- Система отзывов;

### Установка
#### Шаблон файла .env (папка infra-vmeste)
```
SECRET_KEY='django.super.secret.production.key'
TELEGRAM_TOKEN='telegram.token'
SENTRY_DSN='token.to.be.aware.of.problems.in.production'

DEBUG = False
ALLOWED_HOSTS='localhost, 127.0.0.1, <IP.address.or.domain>'

DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST_USER=mail.address
EMAIL_PORT=777
EMAIL_HOST_PASSWORD=mail.password
EMAIL_HOST=your.smtp.server

SOCIAL_AUTH_VK_OAUTH2_KEY='fewdigits'
SOCIAL_AUTH_VK_OAUTH2_SECRET='fewchars'
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY='manychars.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET='few-more-chars'
```
#### Стандартное разворачивание:
```
git clone git@github.com:ratarov/V_MESTE_play.git
py -m venv venv
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
python manage.py start_bot
```
#### Docker:
```
git clone git@github.com:ratarov/V_MESTE_play.git
cd infra-vmeste/
docker-compose up -d
docker exec -it vmeste-back python manage.py collectstatic --no-input
docker exec -it vmeste-back python manage.py migrate
docker exec -d vmeste-back python manage.py start_bot
```
#### Создание суперпользователя с правами администратора, наполнение базы:
Создание Суперпользователя
```
docker exec -it vmeste-back python manage.py createsuperuser
```
База с 1500 игр с tesera.ru
```
docker exec -it vmeste-back python manage.py import_json
```
База с фикстурами: статусы игр, типы мест
```
docker exec -it vmeste-back python manage.py loaddata fixtures.json
```

### Автор
Руслан Атаров