import pytest


import json
import os

from src.json_file import JSONVacancyStorage
from src.vacancy import Vacancy


@pytest.fixture
def vacancies():
    return [
        Vacancy(id="1", name="Python Developer", url="http://example.com/1", currency="RUR",
                description="Python Test description", salary_from=100000, salary_to=150000),
        Vacancy(id="2", name="Java Developer", url="http://example.com/2", currency="RUR",
                description="Java Test description", salary_from=120000, salary_to=170000),
    ]


@pytest.fixture
def json_storage(tmp_path):
    return JSONVacancyStorage(filepath="test.json")


def test_add_vacancies(json_storage, vacancies):
    json_storage.add_vacancies(vacancies)

    saved_vacancies = json_storage.get_vacancies()
    assert len(saved_vacancies) == 2
    assert saved_vacancies[0].id == "1"
    assert saved_vacancies[1].id == "2"


def test_get_vacancies_by_keywords(json_storage, vacancies):
    json_storage.add_vacancies(vacancies)

    found_vacancies = json_storage.get_vacancies_by_keywords(["Python"])
    assert len(found_vacancies) == 1
    assert found_vacancies[0].id == "1"


def test_delete_vacancy(json_storage, vacancies):
    json_storage.add_vacancies(vacancies)

    result = json_storage.delete_vacancy("1")
    assert result is True

    remaining_vacancies = json_storage.get_vacancies()
    assert len(remaining_vacancies) == 1
    assert remaining_vacancies[0].id == "2"


def test_delete_vacancy_not_found(json_storage, vacancies):
    json_storage.add_vacancies(vacancies)

    result = json_storage.delete_vacancy("3")
    assert result is False

