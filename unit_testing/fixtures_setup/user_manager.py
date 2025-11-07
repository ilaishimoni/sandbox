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