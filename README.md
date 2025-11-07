# Pytest introduction - UnitTesting, fixtures, pytest-mock

We are using the *pytest* framework in our automation infrastructure to write our tests.

## Installation

Install pytest with pip:

```bash
pip install pytest
```

Additionally, we will use a plugin for mocking functionality in tests:

```bash
pip install pytest-mock
```

## Usage

Here's a simple example for an assertion which will be picked up by pytest

```python

# content of test_sample.py
def inc(x):
    return x + 1


def test_answer():
    assert inc(3) == 5
```

Then executing this using the ```pytest``` command will result in the following :

    $ pytest
    ============================= test session starts =============================
    collected 1 items

    test_sample.py F

    ================================== FAILURES ===================================
    _________________________________ test_answer _________________________________

        def test_answer():
    >       assert inc(3) == 5
    E       assert 4 == 5
    E        +  where 4 = inc(3)

    test_sample.py:5: AssertionError
    ========================== 1 failed in 0.04 seconds ===========================



UnitTesting
--------
A unit test ensures we get the expected outcome or result from a small unit of code.

```python
class UserManager:
    def __init__(self):
        self.users = {}

    def add_user(self, username, email):
        if username in self.users:
            raise ValueError("User already exists")
        self.users[username] = email
        return True

    def get_user_email(self, username):
        user = self.users.get(username)
        if user:
            return user
        raise ValueError("User does not exist")

    def get_all_users(self):
        return self.users
```

This UserManager class includes multiple methods we will want to test individually

Here is how the unit tests should look like : 

```python
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

```

### The "test" keyword
Pytest will "collect" tests only if their name includes the word "test" in the function name.

### Assertions
The assert keyword simply performs a comparison of the two given arguments,   
If any assertion occurs during the test, the test crashes.

### The raises() function
We are able to expect a specific exception in our testing, as well as the exact content attached to this exception.


## Pytest fixtures

A fixture is a reusable, modular function built into pytest.   
Our tests are meant to be independent, fixtures help us with that by creating a clean objects for the test to use and clean up the changes made by other tests.
The more general usage of a fixture is to handle setup actions ( actions that occur before start of a test ) and teardown actions ( actions that occur before the test ends ).

Example :
```python
def test_add_new_user(user_manager):
    assert user_manager.add_user("Ilai", "ilaishimoni@gmail.com") == True

def test_get_user_email(user_manager):
    user_manager.add_user("Ilai", "ilaishimoni@gmail.com")
    assert user_manager.get_user_email("Ilai") == "ilaishimoni@gmail.com"

```
Both of the tests are interacting with the user_manager class instance, if no cleanup of the function `test_add_new_user` will be performed the function `test_get_user_email` will no be able to register the user, not the expected behavior of the test !.

And so if our `user_manager` instance will be set as follows : 

```python
user_manager = UserManager()
```

our second test will fail

```
unitest.py .F                                                                                                                                                                                                                [100%]

============================================================================================================ FAILURES =============================================================================================================
_______________________________________________________________________________________________________ test_get_user_email _______________________________________________________________________________________________________

    def test_get_user_email():
>       user_manager.add_user("Ilai", "ilaishimoni@gmail.com")

unitest.py:17: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <main.UserManager object at 0x00000282326B4050>, username = 'Ilai', email = 'ilaishimoni@gmail.com'

    def add_user(self, username, email):
        if username in self.users:
>           raise ValueError("User already exists")
E           ValueError: User already exists

main.py:7: ValueError
===================================================================================================== short test summary info =====================================================================================================
FAILED unitest.py::test_get_user_email - ValueError: User already exists

```

Passing the instance to the tests as a fixture solves the issue

```python
@pytest.fixture
def user_manager():
    """Creates a fresh user manager object"""
    return UserManager()

```

```
unitest.py ..                                                                                                                                                                                                                [100%]

======================================================================================================== 2 passed in 0.03s ========================================================================================================
(.venv) PS C:\Users\ilai\PyCharmMiscProject> pytest .\unitest.py
======================================================================================================= test session starts =======================================================================================================
platform win32 -- Python 3.13.5, pytest-8.4.2, pluggy-1.6.0
rootdir: C:\Users\ilai\PyCharmMiscProject
configfile: pyproject.toml
plugins: anyio-4.11.0, mock-3.15.1
collected 2 items                                                                                                                                                                                                                  

unitest.py ..                                                                                                                                                                                                                [100%]

======================================================================================================== 2 passed in 0.02s ========================================================================================================

```
