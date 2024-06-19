import socketdev
from socketdev.tools import load_files


class FullScans:
    @staticmethod
    def get(org_slug: str) -> dict:
        path = "orgs/"+org_slug+"/full-scans"
        headers = None
        payload = None

        response = socketdev.do_request(
            path=path,
            headers=headers,
            payload=payload
        )
        if response.status_code == 200:
            result = response.json()
        else:
            result = {}
        return result

    @staticmethod
    def create_params_string(params: dict) -> str:
        param_str = ""
        for name in params:
            value = params[name]
            param_str += f"&{name}={value}"
        param_str = "?" + param_str.lstrip("&")
        return param_str

    @staticmethod
    def post(
            files: list, 
            params: dict
            ) -> dict:
        
        loaded_files = []
        loaded_files = load_files(files, loaded_files)
        params_arg = FullScans.create_params_string(params)
        path = "orgs/"+params["org_slug"]+"/full-scans"+params_arg

        response = socketdev.do_request(
            path=path,
            method="POST",
            files=loaded_files
        )

        if response.status_code == 201:
            result = response.json()
        else:
            print(f"Error posting {files} to the Fullscans API")
            print(response.text)
            result = response.text
        return result
