from fastapi import status


def test_valid_register_item(app):
    params = {
        "title": "제목",
        "content": "내용",
        "price": 16000
    }

    result = app.post("/auth/item", json=params)
    assert result.status_code == status.HTTP_200_OK
