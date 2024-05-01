# Проект "Анализ вакансий на сайте hh.ru"

## Описание проекта
Проект представляет собой систему для получения данных о работодателях и вакансиях с сайта hh.ru через их публичный API. Полученные данные сохраняются в базе данных PostgreSQL, после чего предоставляются пользователю через класс DBManager.

## Основные шаги проекта
1. Получение данных о работодателях и их вакансиях с сайта hh.ru через API с помощью библиотеки requests.
2. Создание класса DBManager для работы с данными в базе данных.
3. Проектирование таблиц в базе данных PostgreSQL для хранения информации о работодателях и их вакансиях.
4. Выбор 10 интересующих компаний для получения данных о вакансиях.
5. Заполнение созданных таблиц данными о работодателях и их вакансиях.

## Используемые библиотеки
- requests для работы с API hh.ru
- psycopg2 для работы с базой данных PostgreSQL

## Класс DBManager
Класс DBManager предоставляет следующие методы:

- `create_tables()`: Создает таблицы в БД.
- `add_company(company_id, company_name, company_url)`: Заполняет таблицу компаний.
- `add_vacancy(id, company_id, name, responsibility, requirement, salary_from, salary_to, link, experience_required)`: Заполняет таблицу вакансий.
- `get_companies_and_vacancies_count()`: Получает список всех компаний и количество вакансий у каждой компании.
- `get_all_vacancies()`: Получает список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.
- `get_avg_salary()`: Получает среднюю зарплату по вакансиям.
- `get_vacancies_with_higher_salary()`: Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
- `get_vacancies_with_keyword(keyword)`: Получает список всех вакансий, в названии которых содержится переданное ключевое слово.
- `close_connection()`: Закрывает соединение с БД.
## Установка и запуск
1. Установите необходимые библиотеки: `pip install requests psycopg2`
2. Создайте базу данных PostgreSQL и заполните её спарсенными вакансиями, используя функцию `create_db()` из файла main.py.
3. Используйте класс DBManager для анализа данных в базе данных.

## Пример использования класса кода в файле main.py
```python
if __name__ == "__main__":
    
    #Список компаний
    companys = {
        "MTS": 3776,
        "Beeline": 4934,
        "Rostelekom": 2748,
        "Megaphone": 3127,
        "Tele2": 4219,
        "Rosatom": 577743,
        "Gasprom": 39305,
        "Yandex": 1740,
        "Avito": 84585,
        "Ozon": 2180
    }
    #Создание таблицы в БД и ее заполнение
    create_db(companys=companys,
              dbname="hh",
              user="postgresql",
              password="12345",
              host="localhost",
              port=5232)
    #Работа с БД
    try:
        db = DBManager(dbname="hh",
                   user="postgresql",
                   password="12345",
                   host="localhost",
                   port=5232)
        print(db.get_companies_and_vacancies_count())
        print(db.get_all_vacancies())
        print(db.get_avg_salary())
        print(db.get_vacancies_with_higher_salary())
        print(db.get_vacancies_with_keyword("python"))
        db.close_connection()
    except psycopg2.Error as e:
        print("Ошибка соединения с БД: ", e)