import socketdev
from socketdev.tools import load_files
import json


class FullScans:
    @staticmethod
    def get(org_slug: str, params: dict) -> dict:
        params_arg = ""
        for name in params:
            value = params[name]
            if value:
                params_arg += f"&{name}={value}"
        params_arg = "?" + params_arg.lstrip("&")

        path = "orgs/" + org_slug + "/full-scans" + str(params_arg)
        headers = None
        payload = None
        print(path)
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
<<<<<<< HEAD

        params_arg = ""
        for name in params:
            value = params[name]
            if value:
                params_arg += f"&{name}={value}"
        params_arg = "?" + params_arg.lstrip("&")

        path = "orgs/" + str(params["org_slug"]) + "/full-scans" + str(params_arg)
=======
        params_arg = FullScans.create_params_string(params)
        path = "orgs/"+params["org_slug"]+"/full-scans"+params_arg
>>>>>>> d38d1a1a6b6873a9d062a2978a5436dde25997ad

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
<<<<<<< HEAD
    
    @staticmethod
    def delete(org_slug: str, full_scan_id: str) -> dict:
        path = "orgs/" + org_slug + "/full-scans/" + full_scan_id
        print(path)
        response = socketdev.do_request(
            path=path,
            method="DELETE"
        )

        if response.status_code == 200:
            result = response.json()
        else:
            result = {}
        return result

    @staticmethod
    def stream(org_slug: str, full_scan_id: str) -> dict:
        path = "orgs/" + org_slug + "/full-scans/" + full_scan_id
        print(path)
        response = socketdev.do_request(
            path=path,
            method="GET"
        )

        if response.status_code == 200:
            result = response.json()
        else:
            result = {}
        return result
    
    @staticmethod
    def metadata(org_slug: str, full_scan_id: str) -> dict:
        path = "orgs/" + org_slug + "/full-scans/" + full_scan_id + "/metadata"
        print(path)
        response = socketdev.do_request(
            path=path,
            method="GET"
        )

        if response.status_code == 200:
            result = response.json()
        else:
            result = {}
        return result
    
=======
>>>>>>> d38d1a1a6b6873a9d062a2978a5436dde25997ad
