import requests
from dataclasses import dataclass


@dataclass
class HH_API:

    company: str
    url_company: str = "https://api.hh.ru/vacancies?employer_id="

    def fetch_jobs(self):
        try:
            response = requests.get(self.url_company + self.company, params={"per_page": 100})
            response.raise_for_status()
            return response.json()['items']
        except requests.exceptions.HTTPError as http_err:
            # Обработка HTTP ошибок
            print(http_err)
        except requests.exceptions.ConnectionError as conn_err:
            # Обработка ошибок соединения
            print(conn_err)
        except requests.exceptions.Timeout as timeout_err:
            # Обработка ошибки тайм-аута
            print(timeout_err)
        except requests.exceptions.RequestException as req_err:
            # Обработка любых исключений, связанных с запросами
            print(req_err)
        except Exception as e:
            # Обработка всех остальных исключений
            print(f"Произошла ошибка: {e}")
        # Возвращение None в случае возникновения ошибки
        return None

