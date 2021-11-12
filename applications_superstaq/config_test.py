from unittest import mock

import applications_superstaq


def test_service_get_balance() -> None:
    client = applications_superstaq.superstaq_client._SuperstaQClient(
        remote_host="http://example.com", api_key="key", client_name="applications_superstaq"
    )
    service = applications_superstaq.config.Config(client)
    mock_client = mock.MagicMock()
    mock_client.get_balance.return_value = {"balance": 12345.6789}
    service._client = mock_client

    assert service.get_balance() == "$12,345.68"
    assert service.get_balance(pretty_output=False) == 12345.6789


@mock.patch(
    "applications_superstaq.superstaq_client._SuperstaQClient.aqt_upload_configs",
    return_value={"status": "Your AQT configuration has been updated"},
)
def test_service_aqt_upload_configs(mock_aqt_compile: mock.MagicMock) -> None:

    client = applications_superstaq.superstaq_client._SuperstaQClient(
        remote_host="http://example.com", api_key="key", client_name="applications_superstaq"
    )
    service = applications_superstaq.config.Config(client)

    with open("/tmp/Pulses.yaml", "w") as pulses_file:
        pulses_file.write("Hello")

    with open("/tmp/Variables.yaml", "w") as variables_file:
        variables_file.write("World")

    assert service.aqt_upload_configs("/tmp/Pulses.yaml", "/tmp/Variables.yaml") == {
        "status": "Your AQT configuration has been updated"
    }
