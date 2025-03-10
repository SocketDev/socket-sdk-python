import logging
from datetime import datetime, timedelta, timezone
from socketdev.exceptions import APIFailure

log = logging.getLogger("socketdev")


class Report:
    def __init__(self, api):
        self.api = api

    def list(self, from_time: int = None) -> dict:
        """
        This function will return all reports from time specified.
        :param from_time: Unix epoch time in seconds. Will default self, to 30 days
        """
        if from_time is None:
            from_time = int((datetime.now(timezone.utc) - timedelta(days=30)).timestamp())
        else:
            from_time = int((datetime.now(timezone.utc) - timedelta(seconds=from_time)).timestamp())

        path = "report/list"
        if from_time is not None:
            path += f"?from={from_time}"

        try:
            response = self.api.do_request(path=path)
            if response.status_code == 200:
                return response.json()
        except APIFailure as e:
            log.error(f"Socket SDK: API failure while listing reports {e}")
            raise
        except Exception as e:
            log.error(f"Socket SDK: Unexpected error while listing reports {e}")
            raise

        return {}

    def delete(self, report_id: str) -> bool:
        path = f"report/delete/{report_id}"
        try:
            response = self.api.do_request(path=path, method="DELETE")
            if response.status_code == 200:
                return True
        except APIFailure as e:
            log.error(f"Socket SDK: API failure while deleting report {e}")
            raise
        except Exception as e:
            log.error(f"Socket SDK: Unexpected error while deleting report {e}")
            raise

        return False

    def view(self, report_id) -> dict:
        path = f"report/view/{report_id}"
        try:
            response = self.api.do_request(path=path)
            if response.status_code == 200:
                return response.json()
        except APIFailure as e:
            log.error(f"Socket SDK: API failure while viewing report {e}")
            raise
        except Exception as e:
            log.error(f"Socket SDK: Unexpected error while viewing report {e}")
            raise

        return {}

    def supported(self) -> dict:
        path = "report/supported"
        try:
            response = self.api.do_request(path=path)
            if response.status_code == 200:
                return response.json()
        except APIFailure as e:
            log.error(f"Socket SDK: API failure while getting supported files {e}")
            raise
        except Exception as e:
            log.error(f"Socket SDK: Unexpected error while getting supported files {e}")
            raise

        return {}

    def create(self, files: list) -> dict:
        open_files = []
        for name, path in files:
            file_info = (name, (name, open(path, "rb"), "text/plain"))
            open_files.append(file_info)
        path = "report/upload"
        payload = {}

        try:
            response = self.api.do_request(path=path, method="PUT", files=open_files, payload=payload)
            if response.status_code == 200:
                return response.json()
        except APIFailure as e:
            log.error(f"Socket SDK: API failure while creating report {e}")
            raise
        except Exception as e:
            log.error(f"Socket SDK: Unexpected error while creating report {e}")
            raise

        return {}
