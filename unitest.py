import pytest
from main import UserManager

@pytest.fixture
def user_manager():
    """Creates a fresh user manager object"""
    return UserManager()


def test_add_new_user(user_manager):
    assert user_manager.add_user("Ilai", "ilaishimoni@gmail.com") == True

def test_get_user_email(user_manager):
    user_manager.add_user("Ilai", "ilaishimoni@gmail.com")
    assert user_manager.get_user_email("Ilai") == "ilaishimoni@gmail.com"

def test_add_existing_user(user_manager):
    user_manager.add_user("Ilai", "ilaishimoni@gmail.com")
    with pytest.raises(ValueError, match="User already exists"):
        user_manager.add_user("Ilai", "ilaishimoni@gmail.com")

def test_get_non_existing_user(user_manager):
    with pytest.raises(ValueError, match="User does not exist"):
        user_manager.get_user_email("ilaishimoni@gmail.com")

def test_get_multiple_users(user_manager):
    user_manager.add_user("Ilai", "ilaishimoni@gmail.com")
    user_manager.add_user("Dan", "fatdan@gmail.com")

    expected_users = {
        "Ilai": "ilaishimoni@gmail.com",
        "Dan": "fatdan@gmail.com",
    }

    assert user_manager.get_all_users() == expected_users
