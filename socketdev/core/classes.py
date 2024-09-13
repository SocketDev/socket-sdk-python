import json


class Score:
    supplyChain: float
    quality: float
    maintenance: float
    license: float
    overall: float
    vulnerability: float

    def __init__(self, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)
        for score_name in self.__dict__:
            score = getattr(self, score_name)
            if score <= 1:
                score = score * 100
                setattr(self, score_name, score)

    def __str__(self):
        return json.dumps(self.__dict__)


class Package:
    type: str
    name: str
    version: str
    release: str
    id: str
    direct: bool
    manifestFiles: list
    author: list
    size: int
    score: dict
    scores: Score
    alerts: list
    error_alerts: list
    alert_counts: dict
    topLevelAncestors: list
    url: str
    transitives: int
    license: str
    license_text: str
    purl: str

    def __init__(self, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)
        if not hasattr(self, "direct"):
            self.direct = False
        else:
            if str(self.direct).lower() == "true":
                self.direct = True
        self.url = f"https://socket.dev/{self.type}/package/{self.name}/overview/{self.version}"
        if hasattr(self, 'score'):
            self.scores = Score(**self.score)
        if not hasattr(self, "alerts"):
            self.alerts = []
        if not hasattr(self, "topLevelAncestors"):
            self.topLevelAncestors = []
        if not hasattr(self, "manifestFiles"):
            self.manifestFiles = []
        if not hasattr(self, "transitives"):
            self.transitives = 0
        if not hasattr(self, "author"):
            self.author = []
        if not hasattr(self, "size"):
            self.size = 0
        self.alert_counts = {
            "critical": 0,
            "high": 0,
            "middle": 0,
            "low": 0
        }
        self.error_alerts = []
        if not hasattr(self, "license"):
            self.license = "NoLicenseFound"
        if not hasattr(self, "license_text"):
            self.license_text = ""
        self.url = f"https://socket.dev/{self.type}/package/{self.name}/overview/{self.version}"
        self.purl = f"{self.type}/{self.name}@{self.version}"


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

    def json(self):
        return self.__dict__


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
