import pytest
import requests

from src.api import HhAPI


@pytest.fixture
def mock_hh_api(monkeypatch):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    def mock_get(*args, **kwargs):
        return MockResponse({
            'items': [
                {'name': 'Vacancy 1', 'salary': {'from': 1000, 'to': 2000}, 'area': {'name': 'Москва'}, 'alternate_url': 'http://example.com/1'},
                {'name': 'Vacancy 2', 'salary': {'from': 2000, 'to': 3000}, 'area': {'name': 'Москва'}, 'alternate_url': 'http://example.com/2'}
            ]
        }, 200)

    monkeypatch.setattr(requests, 'get', mock_get)


@pytest.mark.parametrize("search_query, expected_len", [
    ('python developer', 2),
    ('java developer', 2)
])
def test_get_vacancies(mock_hh_api, search_query, expected_len):
    api = HhAPI()
    vacancies = api.get_vacancies(search_query)

    assert len(vacancies) == expected_len
    assert vacancies[0]['name'] == 'Vacancy 1'
    assert vacancies[1]['name'] == 'Vacancy 2'
    assert vacancies[0]['salary']['from'] == 1000
    assert vacancies[0]['salary']['to'] == 2000
    assert vacancies[1]['salary']['from'] == 2000
    assert vacancies[1]['salary']['to'] == 3000
    assert vacancies[0]['area']['name'] == 'Москва'
    assert vacancies[1]['area']['name'] == 'Москва'
    assert vacancies[0]['alternate_url'] == 'http://example.com/1'
    assert vacancies[1]['alternate_url'] == 'http://example.com/2'