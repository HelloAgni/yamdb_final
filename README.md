# yamdb_final

![workflow](https://github.com/HelloAgni/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## CI и CD проекта api_yamdb

В проекте yamdb_final произведена настройка для приложения api_yamdb Continuous Integration и Continuous Deployment:
- автоматический запуск тестов,
- обновление образов на Docker Hub,
- автоматический деплой на боевой сервер при пуше в главную ветку master.
---
Проект реализует API для сбора отзывов пользователей на произведения. Произведения делятся на категории:  
- Книги,
- Фильмы,
- Музыка.  

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти. Из пользовательских оценок формируется усреднённая оценка произведения — рейтинг.

---
***Для работы с проектом необходимо выполнить действия, описанные ниже.***
```bash
git clone <project>
cd yamdb_final/infra/
```
**Docker**
```bash
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic  
yes
docker-compose exec web python manage.py import_data  
Y
docker-compose exec web python manage.py createsuperuser
...  
> Superuser created successfully.
```
**http://localhost/admin**
>**Для получения документации по API необходимо открыть в браузере адрес http://localhost/redoc/.**  

GET http://localhost/api/v1/titles  
GET http://localhost/api/v1/titles/1  
GET http://localhost/api/v1/titles/1/reviews  
GET http://localhost/api/v1/titles/5/reviews/6/comments  
GET http://localhost/api/v1/titles/?year=1994  
GET http://localhost/api/v1/titles/?genre=comedy

**POSTMAN**  
Для полноценного использования API необходимо выполнить регистрацию пользователя и получить токен. Инструкция для Postman:

***Регистрация пользователя***  
POST  http://localhost/api/v1/auth/signup/
```json
{
    "email": "tester1@mail.ru",
    "username": "tester1"
}
```
Response status 200 OK ✅
```json
{
    "username": "tester1",
    "email": "tester1@mail.ru"
}
```
**Docker**
```bash
docker-compose exec web ls sent_emails  
> Copy your file.log <20220603-081115-140473090362512.log>
docker-compose exec web cat sent_emails/<PASTE your file log>
> Код подтверждения: 61b-18466437bce...
```
**POSTMAN**  
***Получение токена***
POST  http://localhost/api/v1/auth/token/
```json
{
    "username": "tester1",
    "confirmation_code": "61b-18466437bce..."
}
```
Response status 200 OK ✅
```json
{
    "token": "eyJ0e..........."
}
```
Authorization -> Type 'Bearer Token' -> Token -> eyJ0e.........

***Технологии:***  
Python 3.9, Django 2.2, DRF, Nginx, Docker, Docker-compose, Postgresql, Github Actions.

<!-- ***Боевой сервер:***  
http://redsunset.ddns.net/api/v1/ -->