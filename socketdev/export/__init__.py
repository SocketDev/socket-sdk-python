from urllib.parse import urlencode
from dataclasses import dataclass, asdict
from typing import Optional
import socketdev


@dataclass
class ExportQueryParams:
    author: Optional[str] = None
    project_group: Optional[str] = None
    project_name: Optional[str] = None
    project_version: Optional[str] = None
    project_id: Optional[str] = None

    def to_query_params(self) -> str:
        # Filter out None values and convert to query string
        params = {k: v for k, v in asdict(self).items() if v is not None}
        if not params:
            return ""
        return "?" + urlencode(params)


class Export:
    @staticmethod
    def cdx_bom(org_slug: str, id: str, query_params: Optional[ExportQueryParams] = None) -> dict:
        """
        Export a Socket SBOM as a CycloneDX SBOM
        :param org_slug: String - The slug of the organization
        :param id: String - The id of either a full scan or an sbom report
        :param query_params: Optional[ExportQueryParams] - Query parameters for filtering
        :return:
        """
        path = f"orgs/{org_slug}/export/cdx/{id}"
        if query_params:
            path += query_params.to_query_params()
        result = socketdev.do_request(path=path)
        try:
            sbom = result.json()
            sbom["success"] = True
        except Exception as error:
            sbom = {"success": False, "message": str(error)}
        return sbom

    @staticmethod
    def spdx_bom(org_slug: str, id: str, query_params: Optional[ExportQueryParams] = None) -> dict:
        """
        Export a Socket SBOM as an SPDX SBOM
        :param org_slug: String - The slug of the organization
        :param id: String - The id of either a full scan or an sbom report
        :param query_params: Optional[ExportQueryParams] - Query parameters for filtering
        :return:
        """
        path = f"orgs/{org_slug}/export/spdx/{id}"
        if query_params:
            path += query_params.to_query_params()
        result = socketdev.do_request(path=path)
        try:
            sbom = result.json()
            sbom["success"] = True
        except Exception as error:
            sbom = {"success": False, "message": str(error)}
        return sbom
