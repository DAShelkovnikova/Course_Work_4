
from src.functions import filter_vac_salary, sort_vac_for_salary, top_sort_vac

from src.vacancy import Vacancy

vacancy1 = Vacancy(id='1', name='Python Developer', url='http://example.com/1', currency='RUR', description='Python Test description', salary_from=100000, salary_to=150000)
vacancy2 = Vacancy(id='2', name='Java Developer', url='http://example.com/2', currency='RUR', description='Java Test description', salary_from=120000, salary_to=170000)
vacancy3 = Vacancy(id='3', name='JS Developer', url='http://example.com/3', currency='RUR', description='JS Test description', salary_from=None, salary_to=90000)
vacancy4 = Vacancy(id='4', name='Go Developer', url='http://example.com/4', currency='RUR', description='Go Test description', salary_from=80000, salary_to=None)
vacancies = [vacancy1, vacancy2, vacancy3, vacancy4]


def test_filter_vac_salary_both_defined():
    desired_salary = 130000
    filtered_vacancies = filter_vac_salary(vacancies, desired_salary)
    assert len(filtered_vacancies) == 2
    assert vacancy1 in filtered_vacancies
    assert vacancy2 in filtered_vacancies


def test_filter_vac_salary_only_from_defined():
    desired_salary = 90000
    filtered_vacancies = filter_vac_salary(vacancies, desired_salary)
    assert len(filtered_vacancies) == 2
    assert vacancy3 in filtered_vacancies
    assert vacancy4 in filtered_vacancies


def test_filter_vac_salary_only_to_defined():
    desired_salary = 150000
    filtered_vacancies = filter_vac_salary(vacancies, desired_salary)
    assert len(filtered_vacancies) == 2
    assert vacancy1 in filtered_vacancies
    assert vacancy2 in filtered_vacancies


def test_sort_vac_for_salary():
    sorted_vacancies = sort_vac_for_salary(vacancies)
    assert sorted_vacancies == [vacancy2, vacancy1, vacancy3, vacancy4]


def test_top_sort_vac():
    top_n = 2
    top_sorted_vacancies = top_sort_vac(vacancies, top_n)
    expected_sorted_vacancies = sorted([vacancy2, vacancy1], reverse=True)
    assert len(top_sorted_vacancies) == top_n
    assert sorted(top_sorted_vacancies, reverse=True) == expected_sorted_vacancies