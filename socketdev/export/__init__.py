from socketdev.tools import do_request


class Export:
    @staticmethod
    def cdx_bom(org_slug: str, id: str) -> dict:
        path = f"orgs/{org_slug}/export/cdx/{id}"
        result = do_request(path=path)
        try:
            sbom = result.json()
            sbom["success"] = True
        except Exception as error:
            sbom = {"success": False, "message": str(error)}
        return sbom

    @staticmethod
    def spdx_bom(org_slug: str, id: str) -> bool:
        path = f"orgs/{org_slug}/export/spdx/{id}"
        result = do_request(path=path)
        try:
            sbom = result.json()
            sbom["success"] = True
        except Exception as error:
            sbom = {"success": False, "message": str(error)}
        return sbom
