import socketdev
from socketdev.tools import load_files

class Fullscans:
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
    def post(
            files: list, 
            params: dict
            ) -> dict:
        
        loaded_files = []
        loaded_files = load_files(files, loaded_files)

        params_arg = "?"
        params_arg  = params_arg +"repo="+params["repo"]
        if params["branch"]:
            params_arg  = params_arg +"&branch="+params["branch"]
        if params["commit_message"]:
            params_arg  = params_arg +"&commit_message="+params["commit_message"]
        if params["commit_hash"]:
            params_arg  = params_arg +"&commit_hash="+params["commit_hash"]
        if params["pull_request"]:
            params_arg  = params_arg +"&pull_request="+params["pull_request"]
        if params["committers"]:
            params_arg  = params_arg +"&committers="+params["committers"]
        if params["make_default_branch"]:
            params_arg  = params_arg +"&make_default_branch="+params["make_default_branch"]
        if params["set_as_pending_head"]:
            params_arg  = params_arg +"&set_as_pending_head="+params["set_as_pending_head"]
        if params["tmp"]:
            params_arg  = params_arg +"&tmp="+params["tmp"]

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