import socketdev


class Report:
    @staticmethod
    def list() -> dict:
        path = "report/list"
        response = socketdev.do_request(path=path)
        if response.status_code == 200:
            reports = response.json()
        else:
            reports = {}
        return reports

    @staticmethod
    def delete(report_id: str) -> bool:
        path = f"report/delete/{report_id}"
        response = socketdev.do_request(
            path=path,
            method="DELETE"
        )
        if response.status_code == 200:
            deleted = True
        else:
            deleted = False
        return deleted

    @staticmethod
    def view(report_id) -> dict:
        path = f"report/view/{report_id}"
        response = socketdev.do_request(path=path)
        if response.status_code == 200:
            report = response.json()
        else:
            report = {}
        return report

    @staticmethod
    def supported() -> dict:
        path = "report/supported"
        response = socketdev.do_request(path=path)
        if response.status_code == 200:
            report = response.json()
        else:
            report = {}
        return report

    @staticmethod
    def create(files: list) -> dict:
        open_files = []
        for name, path in files:
            file_info = (name, (name, open(path, 'rb'), 'text/plain'))
            open_files.append(file_info)
        path = "report/upload"
        payload = {}
        response = socketdev.do_request(
            path=path,
            method="PUT",
            files=open_files,
            payload=payload
        )
        if response.status_code == 200:
            reports = response.json()
        else:
            reports = {}
        return reports
