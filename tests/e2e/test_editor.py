import pytest
from fastapi import status
import json
from ..utils import make_expect_result, make_change_history_info
from app.utils.utils import get_current_time


@pytest.fixture
def params():
    return {
        "title": "제목",
        "content": "내용",
        "price": 16000
    }


@pytest.fixture
def setting(app, params):
    result = app.post("/auth/item", json=params)
    assert result.status_code == status.HTTP_200_OK
    return json.loads(result.text)['idx']


@pytest.mark.freeze_time
def test_editor_get_item(app, params, setting):
    expected = [make_expect_result(params, get_current_time(), setting)]
    result = app.get("/editor/item")
    assert json.loads(result.text)['items'] == expected

    params2 = {"title": "TestCase용", "content": "내용2", "price": 100}
    idx = json.loads(app.post("/auth/item", json=params2).text)['idx']

    expected.append(make_expect_result(params2, get_current_time(), idx))

    result = app.get("/editor/item")
    assert json.loads(result.text)['items'] == expected


@pytest.mark.freeze_time
def test_editor_put_item(app, params, setting):
    change_param = {
        "price": 100,
        "fee": 20
    }

    response = app.put(f"/editor/item/{setting}", json=change_param)
    assert response.status_code == status.HTTP_200_OK
    params['price'] = change_param['price']

    expected_info = make_expect_result(params, get_current_time(), json.loads(response.text)['idx'])
    expected_info['updater'] = "Editor"
    expected_info['update_date'] = get_current_time()
    expected_info['fee'] = change_param['fee']

    expected = [expected_info]
    result = app.get("/editor/item")
    assert json.loads(result.text)['items'] == expected


@pytest.mark.freeze_time
def test_editor_wrong_put_item(app, params, setting):
    change_param = {
        "price": 100,
        "fee": 20
    }

    with pytest.raises(Exception) as e:
        response = app.put(f"/editor/item/{setting+20}", json=change_param)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    assert str(e.value) == "해당 아이템을 찾을 수 없습니다."


@pytest.mark.freeze_time
def test_editor_confirmed_put_item(app, params, setting):
    response = app.put(f"/editor/item/confirmed/{setting}")
    assert response.status_code == status.HTTP_200_OK

    params['confirmed_editor'] = "Editor"
    response = app.get("/editor/item")

    expected_info = make_expect_result(params, get_current_time(), setting)

    expected_info['update_date'] = get_current_time()
    expected_info['confirmed_editor'] = "Editor"
    expected_info['EN'] = {
        'item_idx': 1, 'language': 1, 'title': 'Title', 'content': 'Contents', 'idx': 2
    }

    expected_info['CH'] = {
        'item_idx': 1, 'language': 2, 'title': '题目', 'content': '内容', 'idx': 3
    }

    assert json.loads(response.text)['items'] == [expected_info]


@pytest.mark.freeze_time
def test_editor_get_change_history(app, params, setting):
    change_params = {
        'title': "바뀐 제목"
    }

    response = app.put(f"/auth/item/{setting}", json=change_params)
    assert response.status_code == status.HTTP_200_OK

    expected = [make_change_history_info(change_params, get_current_time(), json.loads(response.text)['idx'], setting)]

    response = app.get(f"/editor/change-request/item/{setting}")
    assert json.loads(response.text)['items'] == expected


@pytest.mark.freeze_time
def test_editor_confirmed_change_history(app, params, setting):
    change_params = {
        'title': "바뀐 제목"
    }

    response = app.put(f"/auth/item/{setting}", json=change_params)
    assert response.status_code == status.HTTP_200_OK

    infos = make_change_history_info(change_params, get_current_time(), json.loads(response.text)['idx'], setting)
    infos['confirmed_editor'] = "Confirmed"
    infos['confirmed_date'] = get_current_time()

    response = app.put(f"/editor/change-request/{setting}")
    assert json.loads(response.text)['msg'] == "ok"

    response = app.get(f"/editor/change-request/item/{setting}")
    assert json.loads(response.text)['items'] == [infos]
