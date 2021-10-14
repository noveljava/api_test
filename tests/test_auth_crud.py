import pytest

from app.core.user_manager import UserManager
from app.db.models.user import User
from app.db.repository import SqlAlchemyRepository
from app.routers.models.user import User as RouterUser


@pytest.fixture
def db_handler(session):
    yield SqlAlchemyRepository(session)


@pytest.mark.parametrize("valid_id", ["test1", "TEST1", "tEsT1", "1234567890abcdef"])
def test_valid_signup(db_handler, valid_id):
    password = "test_code"

    request_user = RouterUser(id=valid_id, password=password, name="Test User")
    user_manager = UserManager(db_handler, request_user)
    user_manager.signup()

    expected = [
        User(id=valid_id, password=password, name="Test User"),
    ]

    assert db_handler.session.query(User).all() == expected


@pytest.mark.parametrize("invalid_id", ["a", "ab!", "ab?", "ab*", "1234567890abcdef1"])
def test_invalid_signup(db_handler, invalid_id):
    password = "test_code"

    request_user = RouterUser(id=invalid_id, password=password, name="Test User")
    user_manager = UserManager(db_handler, request_user)

    with pytest.raises(Exception) as e:
        user_manager.signup()

    assert str(e.value) == "Invalid ID Format. Check Please."


def test_duplicated_signup(db_handler):
    uid = "testid"
    password = "test_code"
    db_handler.session.execute(f"INSERT INTO user (id, password) VALUES ('{uid}', '{password}')")

    request_user = RouterUser(id=uid, password=password, name="Test User")
    user_manager = UserManager(db_handler, request_user)

    with pytest.raises(Exception) as e:
        user_manager.signup()

    assert str(e.value) == "Already exists ID."


def test_withdrawal(db_handler):
    from datetime import datetime

    uid = "testuser"
    password = "test_code"

    request_user = RouterUser(id=uid, password=password, name="Test User")
    user_manager = UserManager(db_handler, request_user)
    user_manager.signup()

    current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    user_manager.withdrawal()

    in_db_info = db_handler.session.query(User).filter_by(id=uid).first()
    assert not in_db_info.available
    assert in_db_info.withdrawal_data == current_time


def test_empty_name(db_handler):
    from datetime import datetime

    uid = "testuser"
    password = "test_code"

    request_user = RouterUser(id=uid, password=password)
    user_manager = UserManager(db_handler, request_user)
    with pytest.raises(Exception) as e:
        user_manager.signup()

    assert str(e.value) == "Name field is empty."
