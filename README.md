Тестовое задание:
Создать API для мобильного приложения фитнес трекера.
Пользователь регистрируется в приложении с помощью электронной почты с подтверждением адреса.
Приложение отправляет на сервер отчёты об активности пользователя.
Отчёт содержит следующие данные:
1. Дата и время начала активности;
2. Дата и время окончания активности;
3. Тип активности (ходьба, бег, велосипед);
4. Расстояние;
5. Количество калорий.
Приложение может запрашивать статистику по пользовательским активностям с возможностью агрегирования за час и за сутки.
Используемые технологии: Django, Django Rest Framework, PostgreSQL.
Можно использовать любые дополнительные библиотеки по желанию.

###### **_Install and run app:_**

These tutorial describe how to run application for testing purpose. 
Productive deployment tutorial will presented in next release.

- Install postgres database;
- Create database(DB_NAME);
- Create database user(DB_USER);
- Grant all privileges for user to the database;
- Clone application from git to the local directory, git clone....;
- Create python environment;
- Create env variables in python environment;
List of variables (SEC_KEY='django-insecure-.....', DB_NAME='fitness', 
DB_USER='fitnessuser' , DB_PASS='fit1234',
DB_HOST='localhost', DB_PORT='',EMAIL_HOST_USER="vasypupkin@gmail.com", 
  EMAIL_HOST_PASSWORD='test123', SMTP_SERVER='smtp.gmail.com', SMTP_PORT=587)
- Install python packages from requirements.txt file:
pip install -r requirements.txt;
- Migrate database structure to the database:
python manage.py makemigrations
python manage.py migrate;
- Create superuser, for admin web:
python manage.py createsuperuser;
- Add three action type value(running, bicycle, walking) in the table Acttype.
It's usefully to use for this purpose django web admin interface. 
- Start django server in test mode
python manage.py runserver



###### **_REST API Description:_**

**Register email**

Create user credentials(email, password ...) in database, sent email to verify email address.

Request:

URL: serever_hostname/api/email_register

Method: POST

Headers:

'Content-Type: application/json'

Body:

{
    "email": "Vasyapupkin@list.ru",
    "password": "test123"
}

Success Response:

Code: HTTP 201 Created

Body:

{
    "data": {
        "email": "Vasyapupkin@list.ru"
    }
}


**Verify email**
This endpoint created for activation link in verification email.


**Get token**

Create token for user credentials(email, password). Application vetify 
user credentials(email, password) with databases records and check email verification.
If user athorized app gives access token. 

Request:

URL: serever_hostname/api/get_token

Method: POST

Headers:

'Content-Type: application/json'

Body:

{
    "email": "Vasyapupkin@list.ru",
    "password": "test123"
}

Success Response:

Code: HTTP 200 OK

Body:

{
    "success": "True",
    "status code": 200,
    "message": "Token is generated succesfully",
    "token": ": ASDIkPOSMnm!&*1231234039.DAS;'ALSK;LSD.ASD[AASD;slkda;lkndsjkabhjwb"
}


**Save activities**

Save user activities. Times records (start_time, stop_time) writes in the DateTimeField format,
type_of_activity is string, distance and calories are Integer type.

Request:

URL: serever_hostname/api/save_activities

Method: POST

Headers:

'Content-Type: application/json'
'Authorization: Bearer ASDIkPOSMnm!&*1231234039.DAS;'ALSK;LSD.ASD[AASD;slkda;lkndsjkabhjwb'

Body:

{
    "start_time": "2021-05-27 15:45:21.434638+03",
    "stop_time": "2021-05-27 15:46:21.434638+03",
    "type_of_activity": "bicycle",
    "distance": 100,
    "calories": 10
}

Success Response:

Code: HTTP 201 Created

Body:

{
    "success": "True",
    "status code": 201,
    "message": "Activities saved successfully"
}


**Get activities**

Get agregate statistic for user activities. It's possible to get activities for user during last hour
or during last day. Depends on timedelta(get request parameter) value (day or hour) you can get agrregate statistic
for last day or for last hour.
running_stat in seconds
walking_stat in seconds
bicycle_stat in seconds
distance_summ in metre
calories_summ in calories

Request:

URL: serever_hostname/api/get_activities?timedelta=day

Method: GET

Headers:

'Content-Type: application/json'
'Authorization: Bearer ASDIkPOSMnm!&*1231234039.DAS;'ALSK;LSD.ASD[AASD;slkda;lkndsjkabhjwb'


Success Response:

Code: HTTP 200 OK

Body:

{
    "success": "True",
    "status code": 200,
    "user email": "Vasyapupkin@list.ru",
    "message": "Summary statistic for a day",
    "running_stat": "120.0",
    "walking_stat": "0.0",
    "bicycle_stat": "120.0",
    "distance_summ": 400,
    "calories_summ": 40
}



**Repeat verification email**

If you dont verify email address during registration(Dont  get verify link on your email) you can
repeat verification email by this request.

Request:

URL: serever_hostname/api/email_repeated

Method: POST

Headers:

'Content-Type: application/json'

Body:

{
    "email": "Vasyapupkin@list.ru"
}

Success Response:

Code: HTTP 200 OK

Body:

{
    "data": {
        "email": "Vasyapupkin@list.ru"
    }
}

