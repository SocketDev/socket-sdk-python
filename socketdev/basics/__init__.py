import logging
from typing import Optional, Union
from dataclasses import dataclass, asdict

log = logging.getLogger("socketdev")


@dataclass
class SocketBasicsConfig:
    """Data class representing Socket Basics configuration settings."""
    pythonSastEnabled: bool = False
    golangSastEnabled: bool = False
    javascriptSastEnabled: bool = False
    secretScanningEnabled: bool = False
    trivyImageEnabled: bool = False
    trivyDockerfileEnabled: bool = False
    socketScanningEnabled: bool = False
    socketScaEnabled: bool = False
    additionalParameters: str = ""

    def __getitem__(self, key):
        return getattr(self, key)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "SocketBasicsConfig":
        return cls(
            pythonSastEnabled=data.get("pythonSastEnabled", False),
            golangSastEnabled=data.get("golangSastEnabled", False),
            javascriptSastEnabled=data.get("javascriptSastEnabled", False),
            secretScanningEnabled=data.get("secretScanningEnabled", False),
            trivyImageEnabled=data.get("trivyImageEnabled", False),
            trivyDockerfileEnabled=data.get("trivyDockerfileEnabled", False),
            socketScanningEnabled=data.get("socketScanningEnabled", False),
            socketScaEnabled=data.get("socketScaEnabled", False),
            additionalParameters=data.get("additionalParameters", ""),
        )


@dataclass
class SocketBasicsResponse:
    """Data class representing the response from Socket Basics API calls."""
    success: bool
    status: int
    config: Optional[SocketBasicsConfig] = None
    message: Optional[str] = None

    def __getitem__(self, key):
        return getattr(self, key)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "SocketBasicsResponse":
        return cls(
            config=SocketBasicsConfig.from_dict(data) if data else None,
            success=True,
            status=200,
        )


class Basics:
    """
    Socket Basics API client for managing CI/CD security scanning configurations.
    
    Socket Basics is a security scanning suite that includes:
    - SAST (Static Application Security Testing) for Python, Go, and JavaScript
    - Secret scanning for hardcoded credentials
    - Container security for Docker images and Dockerfiles
    - Socket SCA dependency scanning
    """

    def __init__(self, api):
        self.api = api

    def get_config(
        self, org_slug: str, use_types: bool = False
    ) -> Union[dict, SocketBasicsResponse]:
        """
        Get Socket Basics configuration for an organization.

        Args:
            org_slug: Organization slug
            use_types: Whether to return typed response objects (default: False)

        Returns:
            dict or SocketBasicsResponse: Configuration settings for Socket Basics

        Example:
            >>> basics = socketdev_client.basics
            >>> config = basics.get_config("my-org")
            >>> print(config["pythonSastEnabled"])
            
            >>> # Using typed response
            >>> response = basics.get_config("my-org", use_types=True)
            >>> print(response.config.pythonSastEnabled)
        """
        path = f"orgs/{org_slug}/settings/socket-basics"
        response = self.api.do_request(path=path, method="GET")

        if response.status_code == 200:
            config_data = response.json()
            if use_types:
                return SocketBasicsResponse.from_dict(config_data)
            return config_data

        error_message = response.json().get("error", {}).get("message", "Unknown error")
        log.error(f"Failed to get Socket Basics configuration: {response.status_code}, message: {error_message}")
        
        if use_types:
            return SocketBasicsResponse(
                success=False,
                status=response.status_code,
                config=None,
                message=error_message
            )
        return {}