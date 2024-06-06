import socketdev
import json

class Sbom:
    @staticmethod
    def get_sbom_data(report_id: str) -> list:
        path = f"sbom/view/{report_id}"
        response = socketdev.do_request(path=path)
        if response.status_code == 200:
            sbom = []
            sbom_dict = {}
            data = response.text
            data.strip('"')
            data.strip()
            for line in data.split("\n"):
                if line != '"' and line != "" and line is not None:
                    item = json.loads(line)
                    sbom.append(item)
            for key, val in enumerate(sbom):
                sbom_dict[val['id']] = val
        else:
            sbom_dict = {}
        return sbom_dict