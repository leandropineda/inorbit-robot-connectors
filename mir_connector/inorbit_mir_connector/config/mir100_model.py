# SPDX-FileCopyrightText: 2023 InOrbit, Inc.
#
# SPDX-License-Identifier: MIT

from pydantic import BaseModel, field_validator
from .config_base_model import EdgeConnectorModel
from .utils import read_yaml

# TODO: leverate ruamel.yaml capabilities to add comments to
# the yaml and improve how the default configuration section
# that gets added automatically looks.
default_mir100_config = {
    "inorbit_robot_key": "",
    "location_tz": "America/Los_Angeles",
    "log_level": "INFO",
    "cameras": [],
    "connector_type": "mir100",
    "connector_config": {
        "mir_base_url": "http://localhost:80",
        "mir_username": "",
        "mir_password": "",
        "enable_mission_tracking": True,
        "mir_api_version": "v2.0"
    },
    "user_scripts": {}
}

# Expected values
CONNECTOR_TYPE = "mir100"
MIR_API_VERSION = "v2.0"


class MiR100ConfigModel(BaseModel):
    """
    Specific configuration for MiR100 connector.
    """

    mir_base_url: str
    mir_username: str
    mir_password: str
    mir_api_version: str
    enable_mission_tracking: bool

    @field_validator("mir_api_version")
    def api_version_validation(cls, mir_api_version):
        if mir_api_version != MIR_API_VERSION:
            raise ValueError(
                f"Unexpected MiR API version '{mir_api_version}'. Expected '{MIR_API_VERSION}'"
            )
        return mir_api_version


class MiR100Config(EdgeConnectorModel):
    """
    MiR100 connector configuration schema.
    """

    connector_config: MiR100ConfigModel

    @field_validator("connector_type")
    def connector_type_validation(cls, connector_type):
        if connector_type != CONNECTOR_TYPE:
            raise ValueError(
                f"Unexpected connector type '{connector_type}'. Expected '{CONNECTOR_TYPE}'"
            )
        return connector_type


def load_and_validate(config_filename: str, robot_id: str) -> MiR100Config:
    """
    Loads the configuration file and returns a valid and complete configuration object.
    raises an exception if the arguments or configuration are invalid
    """

    config = read_yaml(config_filename, robot_id)
    return MiR100Config(**config)
