
from datetime import datetime, timedelta, timezone


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
            reports = response.json()
        else:
            reports = {}
        return reports

    def delete(self, report_id: str) -> bool:
        path = f"report/delete/{report_id}"
        response = self.api.do_request(path=path, method="DELETE")
        if response.status_code == 200:
            deleted = True
        else:
            deleted = False
        return deleted

    def view(self, report_id) -> dict:
        path = f"report/view/{report_id}"
        response = self.api.do_request(path=path)
        if response.status_code == 200:
            report = response.json()
        else:
            report = {}
        return report

    def supported(self) -> dict:
        path = "report/supported"
        response = self.api.do_request(path=path)
        if response.status_code == 200:
            report = response.json()
        else:
            report = {}
        return report

    def create(self, files: list) -> dict:
        open_files = []
        for name, path in files:
            file_info = (name, (name, open(path, "rb"), "text/plain"))
            open_files.append(file_info)
        path = "report/upload"
        payload = {}
        response = self.api.do_request(path=path, method="PUT", files=open_files, payload=payload)
        if response.status_code == 200:
            reports = response.json()
        else:
            reports = {}
        return reports
