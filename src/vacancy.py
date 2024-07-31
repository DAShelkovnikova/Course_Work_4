from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Vacancy:
    """
    Класс для работой с полученными вакансиями.
    """
    id: str
    name: str
    url: str
    currency: str
    description: str
    salary_from: Optional[int] = None
    salary_to: Optional[int] = None


    def __lt__(self, other: 'Vacancy') -> bool:
        """Метод сравнивает зарплаты"""
        if not isinstance(other, Vacancy):
            return NotImplemented

        if self.salary_from is None and self.salary_to is None:
            if other.salary_from is None and other.salary_to is None:
                return False
            else:
                return True

        if other.salary_from is None and other.salary_to is None:
            return False

        self_avg_salary = self._average_salary()
        other_avg_salary = other._average_salary()

        return self_avg_salary < other_avg_salary


    def _average_salary(self) -> float:
        """ Вспомогательный метод для сравнения зарплат"""
        if self.salary_from is not None and self.salary_to is not None:
            return (self.salary_from + self.salary_to) / 2
        elif self.salary_from is not None:
            return self.salary_from
        elif self.salary_to is not None:
            return self.salary_to
        else:
            return float('-inf')


    @classmethod
    def cast_to_object_list(cls, data: List[dict]) -> List['Vacancy']:
        """Преобразует список словарей, содержащих данные о вакансиях, извлекает необходимые данные,
        создает новый экземпляр класса Vacancy с этими данными и добавляет его в итоговый список.
        Валидация данных
        """
        vacancies = []
        for item in data:
            if 'salary' not in item or 'snippet' not in item or item['salary']['currency'] != 'RUR':
                continue
            if 'id' not in item or 'name' not in item or 'alternate_url' not in item:
                continue

            salary_from = item['salary']['from']
            salary_to = item['salary']['to']
            currency = item['salary']['currency']
            description = item['snippet']['requirement'] if item['snippet'] else ''
            vacancy = cls(
                id=item['id'],
                name=item['name'],
                url=item['alternate_url'],
                salary_from=salary_from,
                salary_to=salary_to,
                currency=currency,
                description=description if description else ''
            )
            vacancies.append(vacancy)
        return vacancies


    def __str__(self) -> str:
        """Метод для представляния вакансий при печати"""
        return (f'{self.id} | {self.name}\n'
                f'{self.url}\n'
                f'{self.description}\n'
                f'{self.salary_from if self.salary_from else "Не указана"} - '
                f'{self.salary_to if self.salary_to else "Не указана"} '
                f'{self.currency}\n')

