import socketdev


class Repos:
    @staticmethod
    def get(org_slug: str, **kwargs) -> dict[str,]:
        query_params = {}
        if kwargs:
            for key, val in kwargs.keys():
                query_params[key] = val
        if len(query_params) == 0:
            return {}
        path = "orgs/" + org_slug + "/repos"
        if query_params is not None:
            path += "?"
            for param in query_params:
                value = query_params[param]
                path += f"{param}={value}&"
            path = path.rstrip("&")
        response = socketdev.do_request(path=path)
        if response.status_code == 200:
            result = response.json()
        else:
            result = {}
        return result

    @staticmethod
    def repo(org_slug: str, repo_name: str) -> dict:
        path = f"orgs/{org_slug}/repos/{repo_name}"
        response = socketdev.do_request(path=path)
        if response.status_code == 200:
            result = response.json()
        else:
            result = {}
        return result

    @staticmethod
    def delete(org_slug: str, name: str) -> dict:
        path = f"orgs/{org_slug}/repos/{name}"
        response = socketdev.do_request(path=path, method="DELETE")
        if response.status_code == 200:
            result = response.json()
        else:
            result = {}
        return result

    @staticmethod
    def post(org_slug: str, **kwargs) -> dict:
        params = {}
        if kwargs:
            for key, val in kwargs.keys():
                params[key] = val
        if len(params) == 0:
            return {}
        path = "orgs/" + org_slug + "/repos"
        response = socketdev.do_request(
            path=path,
            method="POST",
            payload=params.__dict__
        )
        result = {}
        if response.status_code == 200:
            result = response.json()
        return result

    @staticmethod
    def update(org_slug: str, repo_name: str, **kwargs) -> dict:
        params = {}
        if kwargs:
            for key, val in kwargs.keys():
                params[key] = val
        if len(params) == 0:
            return {}
        path = f"orgs/{org_slug}/repos/{repo_name}"
        response = socketdev.do_request(
            path=path,
            method="POST",
            payload=params.__dict__
        )
        if response.status_code == 200:
            result = response.json()
        else:
            result = {}
        return result
