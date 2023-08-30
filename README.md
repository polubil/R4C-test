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
---

## Quick start

1. Clone this repo:
   ```
   git clone https://github.com/polubil/R4C-test -b task2-dev
   ```

2. Create and activate a venv:
   
   ```
   cd .\R4C-test\
   python -m venv venv
   ./venv/Scripts/Activate | source ./venv/Scripts/Activate.sh
   ```
3. Install dependencies:
   
   ```
   pip install -r requirements.txt
   ```
4. Setting up redis or another message broker. In my case I was using Redis in Docker container.

5. Make migrations and migrate:
    
   ```
   py manage.py makemigrations
   py manage.py migrate
   ```
6. Start the django server:
    
   ```
   py manage.py runserver
   ```

7. Run celery worker and celery beat:
   
   ```
   celery -A robots worker -l info --pool=solo
   celery -A robots beat
   ```

## Usage

1. Go to 'http://127.0.0.1:8000/api/robots/report'

2. Click "Download report" if you see this button. 
   If you see the apology message try to reload the page, report should be generated. 
   In any case the report automatically generating daily at 00:00 GMT+3 (Moscow).

3. If there were robots produced last week (last 7 days), in the downloaded report, 
   you will see sheets with produced models of robots. 
   In each sheet, you will see the rows with model, version, and count of produced robots.
   Otherwise, if there are no robots produced in the last week, the spreadsheet will be with only one empty list with
   title "Sheet".

