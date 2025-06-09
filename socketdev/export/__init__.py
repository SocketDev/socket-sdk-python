from urllib.parse import urlencode
from dataclasses import dataclass, asdict
from typing import Optional
import logging

log = logging.getLogger("socketdev")


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
    def __init__(self, api):
        self.api = api

    def cdx_bom(
        self, org_slug: str, id: str, query_params: Optional[ExportQueryParams] = None, use_types: bool = False
    ) -> dict:
        """
        Export a Socket SBOM as a CycloneDX SBOM
        :param org_slug: String - The slug of the organization
        :param id: String - The id of either a full scan or an sbom report
        :param query_params: Optional[ExportQueryParams] - Query parameters for filtering
        :param use_types: Optional[bool] - Whether to return typed responses
        :return: dict
        """
        path = f"orgs/{org_slug}/export/cdx/{id}"
        if query_params:
            path += query_params.to_query_params()
        response = self.api.do_request(path=path)

        if response.status_code == 200:
            return response.json()
            # TODO: Add typed response when types are defined

        log.error(f"Error exporting CDX BOM: {response.status_code}")
        log.error(response.text)
        return {}

    def spdx_bom(
        self, org_slug: str, id: str, query_params: Optional[ExportQueryParams] = None, use_types: bool = False
    ) -> dict:
        """
        Export a Socket SBOM as an SPDX SBOM
        :param org_slug: String - The slug of the organization
        :param id: String - The id of either a full scan or an sbom report
        :param query_params: Optional[ExportQueryParams] - Query parameters for filtering
        :param use_types: Optional[bool] - Whether to return typed responses
        :return: dict
        """
        path = f"orgs/{org_slug}/export/spdx/{id}"
        if query_params:
            path += query_params.to_query_params()
        response = self.api.do_request(path=path)

        if response.status_code == 200:
            return response.json()
            # TODO: Add typed response when types are defined

        log.error(f"Error exporting SPDX BOM: {response.status_code}")
        log.error(response.text)
        return {}
