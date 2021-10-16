import pytest
import json

from fastapi import status
from app.utils.utils import get_current_time

from copy import deepcopy

@pytest.fixture
def setting(app):
    params = [
        {
            "title": "테스트1",
            "content": "내용1",
            "price": 1000
        },
        {
            "title": "테스트2",
            "content": "내용2",
            "price": 900
        },
        {
            "title": "테스트3",
            "content": "내용3",
            "price": 800
        },
    ]

    for param in params:
        result = app.post("/auth/item", json=param)
        assert result.status_code == status.HTTP_200_OK


@pytest.mark.freeze_time
def test_customer_get_item(app, setting):
    resp = app.get("/customer/item")
    assert json.loads(resp.text)['items'] == []

    resp = app.put("/editor/item/confirmed/2")
    assert resp.status_code == status.HTTP_200_OK

    resp = app.get("/customer/item")
    expect = {
        "price": 900,
        "registrant": "Auth_User",
        "reg_date": get_current_time(),
        "idx": 2,
        "fee": None,
        "confirmed_editor": "Editor",
        "updater": None,
        "update_date": get_current_time(),
        'KO': {
            "item_idx": 2,
            "language": 0,
            "title": "테스트2",
            "content": "내용2",
            "idx": 2
        }
    }

    assert json.loads(resp.text)["items"] == [expect]

    resp = app.get("/customer/item/2?lang=en")
    assert resp.status_code == status.HTTP_200_OK

    en_expect = deepcopy(expect)
    del en_expect['KO']
    en_expect['price'] *= 1.2
    en_expect['EN'] = {
        "item_idx": 2,
        "language": 1,
        "title": "Test 2.",
        "content": "Content 2",
        "idx": 4
    }

    assert json.loads(resp.text)["items"] == [en_expect]

    resp = app.get("/customer/item/2?lang=ch")
    assert resp.status_code == status.HTTP_200_OK

    cn_expect = deepcopy(expect)
    del cn_expect['KO']
    cn_expect['price'] *= 1.6
    cn_expect['CH'] = {
        "item_idx": 2,
        "language": 2,
        "title": "测试2",
        "content": "内容 2",
        "idx": 5
    }

    assert json.loads(resp.text)["items"] == [cn_expect]
