import json
from abc import ABC, abstractmethod
from dataclasses import asdict
from typing import List

from config import OPERATION_PATH
from src.vacancy import Vacancy


class VacancyStorage(ABC):
    @abstractmethod
    def add_vacancies(self, vacancy: Vacancy) -> None:
        pass


    @abstractmethod
    def get_vacancies(self) -> List[Vacancy]:
        pass


    @abstractmethod
    def delete_vacancy(self, vacancy_id: str) -> None:
        pass


class JSONVacancyStorage(VacancyStorage):
    """
    Класс для работы с JSON файлами, определяющий базовые операции с вакансиями: добавление, получение, поиск по ключевым словам и удаление.
    """
    def __init__(self, filepath: str = OPERATION_PATH):
        self.__filepath = filepath


    def add_vacancies(self, vacancies: List[Vacancy]) -> None:
        """Сохранить все вакансии в файл"""
        print(f'\nСохранение {len(vacancies)} вакансий в файл')
        self._save_vacancies(vacancies)


    def get_vacancies(self) -> List[Vacancy]:
        """Получить все вакансии из файла"""
        vacancies = self._load_vacancies()
        return vacancies


    def get_vacancies_by_keywords(self, keywords: List[str]) -> List[Vacancy]:
        """Получить все вакансии из файла по ключевому слову в атрибуте description"""
        vacancies = self._load_vacancies()
        result = []
        for vac in vacancies:
            if any(keyword.lower() in vac.description.lower() for keyword in keywords):
                result.append(vac)
        return result


    def delete_vacancy(self, vacancy_id: str) -> bool:
        """Удалить вакансию из файла по атрибуту id"""
        vacancies = self._load_vacancies()
        new_vacancies = [vac for vac in vacancies if vac.id != vacancy_id]
        if len(new_vacancies) == len(vacancies):
            return False
        self._save_vacancies(new_vacancies)
        return True


    def _load_vacancies(self) -> List[Vacancy]:
        """Метод для десериализации json"""
        try:
            with open(self.__filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Vacancy(**item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []


    def _save_vacancies(self, vacancies: List[Vacancy]) -> None:
        """Метод для сериализации JSON"""
        with open(self.__filepath, 'w', encoding='utf-8') as f:
            json.dump([asdict(vac) for vac in vacancies], f, ensure_ascii=False, indent=4)
