import os
import tempfile
from unittest import mock

import pytest

import applications_superstaq


def test_service_get_balance() -> None:
    client = applications_superstaq.superstaq_client._SuperstaQClient(
        remote_host="http://example.com", api_key="key", client_name="applications_superstaq"
    )
    service = applications_superstaq.user_config.UserConfig(client)
    mock_client = mock.MagicMock()
    mock_client.get_balance.return_value = {"balance": 12345.6789}
    service._client = mock_client

    assert service.get_balance() == "$12,345.68"
    assert service.get_balance(pretty_output=False) == 12345.6789


@mock.patch(
    "applications_superstaq.superstaq_client._SuperstaQClient.ibmq_set_token",
    return_value={"status": "Your IBMQ account token has been updated"},
)
def test_ibmq_set_token(mock_ibmq: mock.MagicMock) -> None:
    client = applications_superstaq.superstaq_client._SuperstaQClient(
        remote_host="http://example.com", api_key="key", client_name="applications_superstaq"
    )
    service = applications_superstaq.user_config.UserConfig(client)
    assert service.ibmq_set_token("valid token") == {
        "status": "Your IBMQ account token has been updated"
    }


@mock.patch(
    "applications_superstaq.superstaq_client._SuperstaQClient.aqt_upload_configs",
    return_value={"status": "Your AQT configuration has been updated"},
)
def test_service_aqt_upload_configs(mock_aqt_compile: mock.MagicMock) -> None:
    client = applications_superstaq.superstaq_client._SuperstaQClient(
        remote_host="http://example.com", api_key="key", client_name="applications_superstaq"
    )
    service = applications_superstaq.user_config.UserConfig(client)

    pulse = tempfile.NamedTemporaryFile("w+", delete=False)
    variable = tempfile.NamedTemporaryFile("w+", delete=False)
    with pulse as pulses_file, variable as variables_file:
        pulses_file.write("Hello")
        variables_file.write("World")
        assert service.aqt_upload_configs(pulse.name, variable.name) == {
            "status": "Your AQT configuration has been updated"
        }
    pulses_file.close()
    variables_file.close()


@mock.patch(
    "applications_superstaq.superstaq_client._SuperstaQClient.aqt_get_configs",
    return_value={"pulses": "Hello", "variables": "World"},
)
def test_service_aqt_get_configs(mock_aqt_compile: mock.MagicMock) -> None:
    client = applications_superstaq.superstaq_client._SuperstaQClient(
        remote_host="http://example.com", api_key="key", client_name="applications_superstaq"
    )
    service = applications_superstaq.user_config.UserConfig(client)

    pulses_file = tempfile.NamedTemporaryFile("w+", delete=False)
    variables_file = tempfile.NamedTemporaryFile("w+", delete=False)

    service.aqt_download_configs(pulses_file.name, variables_file.name, overwrite=True)

    with pulses_file as pulse, variables_file as variable:
        assert pulse.read() == "Hello"
        assert variable.read() == "World"

    with pytest.raises(ValueError, match="exist"):
        service.aqt_download_configs(pulses_file.name, variables_file.name)

    service.aqt_download_configs(pulses_file.name, variables_file.name, overwrite=True)

    with pytest.raises(ValueError, match="exists"):
        os.remove(pulses_file.name)
        service.aqt_download_configs(pulses_file.name, variables_file.name)

    os.remove(variables_file.name)

    with pytest.raises(ValueError, match="exists"):
        service.aqt_download_configs(pulses_file.name, variables_file.name)
        os.remove(variables_file.name)
        service.aqt_download_configs(pulses_file.name, variables_file.name)
