import json
from copy import deepcopy
from typing import Dict

import pytest
from fastapi import status
from datetime import datetime


@pytest.fixture
def params() -> Dict:
    return {
        "title": "제목",
        "content": "내용",
        "price": 16000
    }


def test_valid_register_item(app, params):
    result = app.post("/auth/item", json=params)
    assert result.status_code == status.HTTP_200_OK


def test_invalid_register_item(app, params):
    for key in params.keys():
        invalid_params = deepcopy(params)
        del invalid_params[key]
        result = app.post("/auth/item", json=invalid_params)
        assert result.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


def make_expect_result(params, reg_time, idx):
    expected = {
        'price': params['price'], 'registrant': 'Auth_User', 'reg_date': reg_time, 'idx': idx,
        'fee': None,
        'confirmed_editor': None, 'updater': None, 'update_date': None,
        'KO': {
            'item_idx': idx, 'language': 0, 'title': params['title'], 'content': params['content'], 'idx': idx
        }
    }
    return expected


@pytest.mark.freeze_time
def test_get_item(app, params):
    # 등록을 하고 한다.
    current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    response = app.post("/auth/item", json=params)
    item_idx = json.loads(response.text)['idx']

    response = app.get(f"/auth/item/{item_idx}")
    assert response.status_code == status.HTTP_200_OK

    expect = [
       make_expect_result(params, current_time, item_idx)
    ]

    assert json.loads(response.text)['items'] == expect

    params = {
        "title": "제목2",
        "content": "내용2",
        "price": 100
    }

    response = app.post("/auth/item", json=params)
    item_idx = json.loads(response.text)['idx']

    expect.append(make_expect_result(params, current_time, item_idx))
    response = app.get(f"/auth/item/{item_idx}")
    assert response.status_code == status.HTTP_200_OK
    assert json.loads(response.text)['items'] == [expect[1]]

    response = app.get(f"/auth/item")
    assert response.status_code == status.HTTP_200_OK
    assert json.loads(response.text)['items'] == expect


def test_get_item_empty(app):
    # 존재하지 않은 데이터값.
    response = app.get(f"/auth/item/0")
    assert response.status_code == status.HTTP_200_OK
    assert json.loads(response.text)['items'] == []

    response = app.get(f"/auth/item")
    assert response.status_code == status.HTTP_200_OK
    assert json.loads(response.text)['items'] == []


@pytest.mark.freeze_time
def test_update_item(app, params):
    def make_change_history_info(change_infos, reg_date, idx, p_item_idx) -> Dict:
        result = {
            "item_idx": p_item_idx,
            "registrant": "Auth_User",
            "reg_date": reg_date,
            "idx": idx,
            "title": None,
            "content": None,
            "price": None,
            "fee": None
        }

        for key, value in change_infos.items():
            result[key] = value

        return result

    response = app.post("/auth/item", json=params)
    item_idx = json.loads(response.text)['idx']

    expected = []
    current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    change_params = {
        'title': "바뀐 제목"
    }

    response = app.put(f"/auth/item/{item_idx}", json=change_params)
    assert response.status_code == status.HTTP_200_OK

    print("Text]   ", response.text)
    expected.append(make_change_history_info(change_params, current_time, json.loads(response.text)['idx'], item_idx))

    change_params = {
        'price': 2000
    }

    response = app.put(f"/auth/item/{item_idx}", json=change_params)
    assert response.status_code == status.HTTP_200_OK
    expected.append(make_change_history_info(change_params, current_time, json.loads(response.text)['idx'], item_idx))

    response = app.get(f"/auth/change-history/item/{item_idx}")
    print(json.loads(response.text)['items'])
    assert json.loads(response.text)['items'] == expected
