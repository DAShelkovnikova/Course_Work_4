from typing import List
from src.api import HhAPI
from src.json_file import JSONVacancyStorage
from src.vacancy import Vacancy


def filter_vac_salary(vacancies: List[Vacancy], desired_salary: int) -> List[Vacancy]:
    """
    Функция фильтрации списка экземпляров Vacancy на основе введенной от пользователя зарплаты (desired_salary)
    """
    filtered_vacancies = []

    for vac in vacancies:

        if vac.salary_from is not None and vac.salary_to is not None:
            if vac.salary_from <= desired_salary <= vac.salary_to:
                filtered_vacancies.append(vac)

        elif vac.salary_from is not None:
            if vac.salary_from <= desired_salary <= vac.salary_from + 10000:
                filtered_vacancies.append(vac)

        elif vac.salary_to is not None:
            if vac.salary_to - 10000 <= desired_salary <= vac.salary_to:
                filtered_vacancies.append(vac)

    return filtered_vacancies


def sort_vac_for_salary(data: List[Vacancy]) -> List[Vacancy]:
    """Функция сортировки для вакансий по убыванию"""
    return sorted(data, reverse=True)


def top_sort_vac(data: List[Vacancy], top_n: int) -> List[Vacancy]:
    """Функция возвращает 5 первых элементов вакансий"""
    return data[:top_n]


def print_vac(data: List[Vacancy]) -> None:
    """Функция для печати найденных вакансий вакансий"""
    for vac in data:
        print(vac)
    print(f'\nНайдено {len(data)} вакансии\n')


def overwrite_file(json_storage: JSONVacancyStorage, data: List[Vacancy]) -> None:
    """Функция взаимодействия с пользователем, которая запускает процесс записи вакансий в файл"""
    user_choice = input('Сохранить в файле только полученные вакансии? (Да/Нет)  ').lower()
    if user_choice == 'Да':
        json_storage.add_vacancies(data)


def user_interaction() -> None:
    """
    Основная функция взаимодействия с пользователем.
    """
    hh_api = HhAPI()
    json_storage = JSONVacancyStorage()

    print('Добро пожаловать!')
    search_query = input('Введите поисковый запрос: ')
    data = hh_api.get_vacancies(search_query)
    vac_data = Vacancy.cast_to_object_list(data)
    json_storage.add_vacancies(vac_data)

    while True:
        print('\n1. Получить все вакансии из файла')
        print('2. Получить топ вакансий по зарплате')
        print('3. Получить вакансии по желаемой зарплате')
        print('4. Получить вакансии с ключевым словом в описании')
        print('5. Удалить вакансию')
        print('6. Выход\n')

        user_choice = input('Выберите опцию: ')
        if user_choice == '1':
            data_to_print = json_storage.get_vacancies()
            print_vac(data_to_print)
        elif user_choice == '2':
            menu_top_n_vac(json_storage)
        elif user_choice == '3':
            menu_get_vac_for_salary(json_storage)
        elif user_choice == '4':
            menu_get_vac_for_keyword(json_storage)
        elif user_choice == '5':
            menu_delete_vacancy(json_storage)
        elif user_choice == '6':
            print('\nПока!')
            break
        else:
            print('Неверно введено значение. Попрбуйте еще раз\n')


def menu_top_n_vac(json_storage: JSONVacancyStorage) -> None:
    """
    Дополнительная фунция взаимодесвтия с пользователем при выборе 'Вывод топ N вакансий по зарплате'
    Сортирует вакансии по убыванию зарплаты выводит их топ N.
    """
    data = json_storage.get_vacancies()
    n = input(f'\nВведите количество вакансий для показа: ')
    if not n.isdigit():
        print('\nНеобходимо ввести число')
        return
    sort_data = sort_vac_for_salary(data)
    top_n = top_sort_vac(sort_data, int(n))
    print_vac(top_n)
    if top_n:
        overwrite_file(json_storage, top_n)


def menu_get_vac_for_keyword(json_storage: JSONVacancyStorage) -> None:
    """
    Дополнительная функция для взаимодествия с пользователем при выборе 'Получить вакансии с ключевым словом в описании'
    Выводит вакансии по ключевому слову введенном пользователем из атрибута Vacancy.description
    """
    keywords = input('\nВведите ключевые слова через пробел: ').split()
    vacancies = json_storage.get_vacancies_by_keywords(keywords)
    if vacancies:
        print_vac(vacancies)
        overwrite_file(json_storage, vacancies)
    else:
        print('\nВакансии по данным ключевым словам не найдены')


def menu_delete_vacancy(json_storage: JSONVacancyStorage) -> None:
    """
    Дополнительная функция для взаимодествия с пользователем при выборе 'Удалить вакансию'
    Удаляет вакансию по введенному пользователем id с выводом сообщения об удачном удалении
    """
    vac_for_del = json_storage.get_vacancies()
    print_vac(vac_for_del)
    vacancy_id = input('Введите id вакансии, которую хотите удалить: ')
    if json_storage.delete_vacancy(vacancy_id):
        print(f'\nВакансия с id {vacancy_id} удалена')
    else:
        print(f'\nВакансия с id {vacancy_id} не найдена')


def menu_get_vac_for_salary(json_storage: JSONVacancyStorage) -> None:
    """
    Дополнительная функция для взаимодествия с пользователем при выборе 'Получить вакансии по желаемой зарплате'
    Выводит вакансии по введенной пользователем зарплаты.
    """
    salary_input = input('Введите желаемую зарплату: ')

    if not salary_input.isdigit():
        print('Пожалуйста, введите корректное числовое значение зарплаты')
        return

    desired_salary = int(salary_input)
    vacancies = json_storage.get_vacancies()
    filtered_vacancies = filter_vac_salary(vacancies, desired_salary)

    if filtered_vacancies:
        print_vac(filtered_vacancies)
        overwrite_file(json_storage, filtered_vacancies)
    else:
        print('Вакансии по данной зарплате не найдены')
