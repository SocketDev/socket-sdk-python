import socketdev
from socketdev.tools import load_files
import json

class FullScans:

    @staticmethod
    def create_params_string(
                            params: dict
                            ) -> str:
        
        param_str = ""

        for name in params:
            value = params[name]
            if value:
                param_str += f"&{name}={value}"

        param_str = "?" + param_str.lstrip("&")

        return param_str
    
    @staticmethod
    def get(
            org_slug: str, 
            params: dict) -> dict:
        
        params_arg = FullScans.create_params_string(params)

        path = "orgs/" + org_slug + "/full-scans" + str(params_arg)
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
    def post(
            files: list, 
            params: dict
            ) -> dict:
        
        loaded_files = []
        loaded_files = load_files(files, loaded_files)

        params_arg = FullScans.create_params_string(params)

        path = "orgs/" + str(params["org_slug"]) + "/full-scans" + str(params_arg)

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
    
    @staticmethod
    def delete(org_slug: str, 
               full_scan_id: str) -> dict:
        
        path = "orgs/" + org_slug + "/full-scans/" + full_scan_id

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
    def stream(org_slug: str, 
               full_scan_id: str) -> dict:
        
        path = "orgs/" + org_slug + "/full-scans/" + full_scan_id

        response = socketdev.do_request(
            path=path,
            method="GET"
        )

        if response.status_code == 200:
            stream_str = []
            stream_dict = {}
            result = response.text
            result.strip('"')
            result.strip()
            for line in result.split("\n"):
                if line != '"' and line != "" and line is not None:
                    item = json.loads(line)
                    stream_str.append(item)
            for val in stream_str:
                stream_dict[val['id']] = val
        else:
            stream_dict = {}

        return stream_dict
    
    @staticmethod
    def metadata(org_slug: str, 
                 full_scan_id: str) -> dict:
        
        path = "orgs/" + org_slug + "/full-scans/" + full_scan_id + "/metadata"

        response = socketdev.do_request(
            path=path,
            method="GET"
        )

        if response.status_code == 200:
            result = response.json()
        else:
            result = {}

        return result
