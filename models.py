class User:

    def __init__(self, uid: str, uname: str, status: int = 0):
        self.user_id = uid
        self.username = uname
        self.status = status

    def change_status(self, status):
        self.status = status


class Counter:

    def __init__(self, cid: str, name: str, user: User, value: str = 0):
        self.counter_id = cid
        self.name = name
        self.value = value
        self.owner = user

    def increment(self, i=1):
        self.value += i
