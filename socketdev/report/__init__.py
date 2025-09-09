import logging
from datetime import datetime, timedelta, timezone

log = logging.getLogger("socketdev")

# TODO: Add response type classes for Report endpoints


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
        response = self.api.do_request(path=path)
        if response.status_code == 200:
            return response.json()
        log.error(f"Error listing reports: {response.status_code}")
        log.error(response.text)
        return {}

    def delete(self, report_id: str) -> bool:
        path = f"report/delete/{report_id}"
        response = self.api.do_request(path=path, method="DELETE")
        if response.status_code == 200:
            return True
        log.error(f"Error deleting report: {response.status_code}")
        log.error(response.text)
        return False

    def view(self, report_id) -> dict:
        path = f"report/view/{report_id}"
        response = self.api.do_request(path=path)
        if response.status_code == 200:
            return response.json()
        log.error(f"Error viewing report: {response.status_code}")
        log.error(response.text)
        return {}

    def supported(self) -> dict:
        path = "report/supported"
        response = self.api.do_request(path=path)
        if response.status_code == 200:
            return response.json()
        log.error(f"Error getting supported reports: {response.status_code}")
        log.error(response.text)
        return {}

    def create(self, files: list) -> dict:
        # Handle both file path strings and file tuples
        open_files = []
        for file_entry in files:
            if isinstance(file_entry, tuple) and len(file_entry) == 2:
                name, file_data = file_entry
                if isinstance(file_data, tuple) and len(file_data) == 2:
                    # Format: [("field_name", ("filename", file_obj))]
                    filename, file_obj = file_data
                    file_info = (name, (filename, file_obj, "text/plain"))
                    open_files.append(file_info)
                else:
                    # Format: [("field_name", "file_path")]
                    file_info = (name, (name, open(file_data, "rb"), "text/plain"))
                    open_files.append(file_info)
            else:
                # Handle other formats if needed
                log.error(f"Unexpected file format: {file_entry}")
                return {}
                
        path = "report/upload"
        payload = {}
        response = self.api.do_request(path=path, method="PUT", files=open_files, payload=payload)
        if response.status_code in (200, 201):
            return response.json()
        log.error(f"Error creating report: {response.status_code}")
        log.error(response.text)
        return {}
