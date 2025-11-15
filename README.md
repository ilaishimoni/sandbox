# Pytest introduction - UnitTesting, fixtures, parameterize, pytest-mock

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
from user_manager import UserManager

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
Pytest will "collect" tests only if their name includes the word ```test``` in the function name.

### Assertions
The assert keyword simply performs a comparison of the two given arguments,   
If any assertion occurs during the test, the test crashes.

### The raises() function
We are able to expect a specific exception in our testing, as well as the exact content attached to this exception.

## Pytest fixtures - Setup

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
Both of the tests are interacting with the user_manager class instance, if no cleanup of the function `test_add_new_user` will be performed, the function `test_get_user_email` will not be able to register the user, not the expected behavior of the test.

And so if our `user_manager` will be set as a global variable ( and not received as a param ) 

```python
user_manager = UserManager()
```

our second test will fail :

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

Passing the instance to the tests as a fixture solves the issue - making sure a clean object is used.

```python
@pytest.fixture
def user_manager():
    """Creates a fresh user manager object"""
    return UserManager()

```

```
unitest.py ..                                                                                                                                                                                                                [100%]

======================================================================================================== 2 passed in 0.02s ========================================================================================================

```

## Pytest Fixtures - Teardown

The fixture function can also be used to clean up a test after it is done.

Example :

Given a database :

```python
class Database:
    """Simulates a basic user database"""
    def __init__(self):
        self.data = {} # Simulating an in-memory database

    def add_user(self, user_id, name):
        if user_id in self.data:
            raise ValueError("User already exists")
        self.data[user_id] = name

    def get_user(self, user_id):
        return self.data.get(user_id, None)

    def delete_user(self, user_id):
        if user_id in self.data:
            del self.data[user_id]

```

We will want to create tests and ensuring that we clean up the DB after every test

```python
@pytest.fixture

from database import Database

def db():
    """Provides a fresh instance of the Database class and cleans up after the test."""
    database = Database()
    yield database # Provide the fixture instance
    database.data.clear() #Cleanup step ( not needed for in-memory, but useful for real DBs )

def test_add_user(db):
    db.add_user(1, "Alice")
    assert db.get_user(1) == "Alice"

def test_add_duplicate_user(db):
    db.add_user(1, "Alice")
    with pytest.raises(ValueError, match="User already exists"):
        db.add_user(1, "Bob")

def test_delete_user(db):
    db.add_user(2, "Bob")
    db.delete_user(2)
    assert db.get_user(2) is None
```

the cleanup part of the fixture is not really used here, but can be useful   
for performing a database cleanup after every test.

### yield keyword
The yield keyword separates the cleanup actions apart from the teardown actions,    
yield in Python turns a function into a generator — a function that can pause, return a value,   
and then resume exactly where it left off the next time it is called.


## Parametrize

The parametrize decorator allows us to run the same test function multiple times with different inputs.

it saves repetitiveness in our code and allows for a simpler testing infrastructure.

For example testing the following function in different cases :

```python
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int ( n ** 0.5 ) + 1 ):
        if n % i == 0:
            return False
    return True
```

Testing the function for many different cases can be done easily :
```python
import pytest
from is_prime import is_prime


@pytest.mark.parametrize("num, expected", [
    (1, False),
    (2, True),
    (3, True),
    (4, False),
    (17, True),
    (18, False),
    (19, True),
    (25, False),
])
def test_is_prime(num, expected):
    assert is_prime(num) == expected
```

```
unit_testing\parameterize\test_is_prime.py ........                                                                                                                                                                          [100%]

======================================================================================================== 8 passed in 0.04s =======================================================================================================
```

