from typing import Literal

IntegrationType = Literal["api", "github", "gitlab", "bitbucket", "azure"]
INTEGRATION_TYPES = ("api", "github", "gitlab", "bitbucket", "azure")


class Utils:
    @staticmethod
    def validate_integration_type(integration_type: str) -> IntegrationType:
        if integration_type not in INTEGRATION_TYPES:
            raise ValueError(f"Invalid integration type: {integration_type}")
        return integration_type  # type: ignore
