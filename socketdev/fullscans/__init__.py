import socketdev


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
    
    def post(org_slug: str) -> dict:
        path = "orgs/"+org_slug+"/full-scans"
        headers = {
            "accept": "application/json",
            "content-type": "multipart/form-data"
        }
        payload = None

        response = socketdev.do_request(
            path=path,
            method="POST",
            headers=headers,
            payload=payload
        )
        if response.status_code == 200:
            result = response.text
        else:
            print(f"Error posting {org_slug} to the Fullscans API")
            print(response.text)
        return result