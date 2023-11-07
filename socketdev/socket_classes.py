import json


class Dependency:
    branch: str
    id: int
    name: str
    type: str
    version: str
    namespace: str
    repository: str

    def __init__(self, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

    def __str__(self):
        return json.dumps(self.__dict__)


class Org:
    id: int
    image: str
    name: str
    plan: str

    def __init__(self, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

    def __str__(self):
        return json.dumps(self.__dict__)


class Response:
    text: str
    error: bool
    status_code: int

    def __init__(self, text: str, error: bool, status_code: int):
        self.text = text
        self.error = error
        self.status_code = status_code

    def __str__(self):
        return json.dumps(self.__dict__)


class DependGetData:
    url: str
    headers: dict
    payload: str

    def __init__(self, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

    def __str__(self):
        return json.dumps(self.__dict__)
