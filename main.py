import psycopg2

from request_job import HH_API
from db_manager import DBManager


def create_db(companys: dict, dbname: str, user: str, password: str, host: str, port: int):
    try:
        #Создаем таблицу
        data_base = DBManager(dbname=dbname, user=user, password=password, host=host, port=port)
        data_base.create_tables()
        #Заполняем данными
        for value in companys.values():
            hh = HH_API(company=str(value)).fetch_jobs()
            # Company table
            company_id = hh[0].get('employer').get('id')
            company_name = hh[0].get('employer').get('name')
            company_url = hh[0].get('employer').get('alternate_url')
            data_base.add_company(company_id, company_name, company_url)

            for i in hh:
                # Vacancies table
                id = i.get('id')
                name = i.get('name')
                responsibility = i.get('snippet').get('responsibility')
                requirement = i.get('snippet').get('requirement')
                salary_from = i['salary']['from'] if i.get('salary') else None
                salary_to = i['salary']['to'] if i.get('salary') else None
                link = i.get('alternate_url')
                experience_required = i.get('experience').get('name')
                data_base.add_vacancy(id, company_id, name, responsibility, requirement, salary_from, salary_to, link,
                                      experience_required)
        #Закрываем соединение
        data_base.close_connection()
    except psycopg2.Error as e:
        print("Ошибка соединения с БД: ", e)


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


