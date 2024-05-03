import psycopg2


class DBManager:
    def __init__(self, dbname: str, user: str, password: str, host: str, port: int):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                url VARCHAR(255)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vacancies (
                id INTEGER PRIMARY KEY,
                company_id INT REFERENCES companies(id),
                name VARCHAR(255) NOT NULL,
                responsibility TEXT,
                requirement TEXT,
                salary_from NUMERIC NULL,
                salary_to NUMERIC NULL,
                link VARCHAR(255),
                experience_required VARCHAR(255)
            )
        ''')
        self.conn.commit()

    def add_company(self, company_id: int, company_name: str, company_url: str):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO companies (id, name, url)
            VALUES (%s, %s, %s)
        ''', (company_id, company_name, company_url))
        self.conn.commit()

    def add_vacancy(self, id: int, company_id: int, name: str, responsibility: str, requirement: str, salary_from: float, salary_to: float, link: str, experience_required: str):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO vacancies (id, company_id, name, responsibility, requirement, salary_from, salary_to, link, experience_required)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (id, company_id, name, responsibility, requirement, salary_from, salary_to, link, experience_required))
        self.conn.commit()

    def get_companies_and_vacancies_count(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT companies.name, COUNT(vacancies.id) AS vacancy_count
            FROM companies
            LEFT JOIN vacancies ON companies.id = vacancies.company_id
            GROUP BY companies.name
        ''')
        return cursor.fetchall()

    def get_all_vacancies(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT companies.name, vacancies.name, vacancies.salary_from, vacancies.salary_to, vacancies.link
            FROM vacancies
            LEFT JOIN companies ON vacancies.company_id = companies.id
        ''')
        return cursor.fetchall()

    def get_avg_salary(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT AVG(salary_from + salary_to) / 2 AS avg_salary
            FROM vacancies
        ''')
        return cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT companies.name, vacancies.name, vacancies.salary_from, vacancies.salary_to, vacancies.link
            FROM vacancies
            LEFT JOIN companies ON vacancies.company_id = companies.id
            WHERE (vacancies.salary_from + vacancies.salary_to) / 2 > %s
        ''', (avg_salary,))
        return cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword: str):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT companies.name, vacancies.name, vacancies.salary_from, vacancies.salary_to, vacancies.link
            FROM vacancies
            LEFT JOIN companies ON vacancies.company_id = companies.id
            WHERE vacancies.name ILIKE %s
        ''', ('%' + keyword + '%',))
        return cursor.fetchall()

    def close_connection(self):
        self.conn.close()

