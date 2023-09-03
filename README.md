# R4C - Robots for consumers

## Небольшая предыстория.
Давным-давно, в далёкой-далёкой галактике, была компания производящая различных 
роботов. 

Каждый робот(**Robot**) имел определенную модель выраженную двух-символьной 
последовательностью(например R2). Одновременно с этим, модель имела различные 
версии(например D2). Напоминает популярный телефон различных моделей(11,12,13...) и его версии
(X,XS,Pro...). Вне компании роботов чаще всего называли по серийному номеру, объединяя модель и версию(например R2-D2).

Также у компании были покупатели(**Customer**) которые периодически заказывали того или иного робота. 

Когда роботов не было в наличии - заказы покупателей(**Order**) попадали в список ожидания.

---
## Что делает данный код?
Это заготовка для сервиса, который ведет учет произведенных роботов,а также 
выполняет некие операции связанные с этим процессом.

Сервис нацелен на удовлетворение потребностей трёх категорий пользователей:
- Технические специалисты компании. Они будут присылать информацию
- Менеджмент компании. Они будут запрашивать информацию
- Клиенты. Им будут отправляться информация
___

## Как с этим работать?
- Создать для этого проекта репозиторий на GitHub
- Открыть данный проект в редакторе/среде разработки которую вы используете
- Ознакомиться с задачами в файле tasks.md
- Написать понятный и поддерживаемый код для каждой задачи 
- Сделать по 1 отдельному PR с решением для каждой задачи
- Прислать ссылку на своё решение


## Quick start

1. Clone this repo:

   ```
   git clone https://github.com/polubil/R4C-test -b task3-dev
   ```
2. Create and activate the venv:
   
   ```
   cd .\R4C-test\
   python -m venv venv
   ./venv/Scripts/Activate | source ./venv/Scripts/Activate.sh
   ```
3. Install dependencies:
   
   ```
   pip install -r requirements.txt
   ```
4. Create .env file in the root directory and fill it with:
   
   ```
   EMAIL_HOST_USER = 'YOUR EMAIL'
   EMAIL_HOST_PASSWORD = 'YOUR_EMAIL_PASSWORD'
   ```
5. Setting up redis or another message broker. In my case i was using Redis in Docker container.
   
6. Configure django project settings in R4C/settings.py:
    
   ```
   - EMAIL_HOST = 'YOUR_SMTP_HOST'
   - CELERY_BROKER_URL = 'YOUR_BROKER_URL'
   ```
7. Make migrations and migrate:
    
   ```
   py manage.py makemigrations
   py manage.py migrate
   ```
8. Start the django server:
    
   ```
   py manage.py runserver
   ```

9. Run celery worker:
   
   ```
   celery -A customers worker -l info --pool=solo
   ```

## Usage

Send POST request to api/robots/new to add a robot. Provide this in body:
```
{"model":"Il","version":"ya","created":"2003-05-26 10:30:00"}
```

If there is an order for robot with this serial, a mail with text to customer's email will be send:
```
Добрый день!
Недавно вы интересовались нашим роботом модели Il, версии ya. 
Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами
```

You can add orders and customers by the shell:
```
> py manage.py shell

from customers.models import Customer
from orders.models import Order
cust = Customer(email="hello@world.com")
cust.save()
ord = Order(robot_serial="Il-ya", customer=cust)
ord.save()
```
