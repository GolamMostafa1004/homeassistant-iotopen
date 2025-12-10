IoT Open - Home Assistant Integration

A custom Home Assistant integration for IoT Open (Lynx) that enables full interaction between your Lynx installation and Home Assistant using the REST API.

This integration allows you to:

Connect your IoT Open installation to Home Assistant

•	Discover FunctionX objects as Home Assistant entities

•	Retrieve live data via the Status API

•	Manage DeviceX and FunctionX directly from Home Assistant

•	Assign metadata, units, names, device IDs, icons, and more

The integration follows official Home Assistant development patterns, including config_flow, DataUpdateCoordinator, translations, and service definitions.

•	Features
•	Data Model

One HA config entry = one IoT Open installation

DeviceX → Physical devices in IoT Open (e.g., KNX gateways, IoT controllers, sensor hubs)

FunctionX → Logical datapoints (temperature, humidity, switch, boolean, etc.)

Status API → Retrieves live values based on topic_read

What the Integration Does

Uses IoT Open API v2 over HTTPS with X-API-Key authentication

Periodically:

Lists FunctionX for the installation

Reads meta.topic_read for each function

Fetches latest status samples

Creates/updates Home Assistant entities

Automatically groups entities:

If meta.device_id is set → entities grouped under the correct DeviceX

Otherwise → grouped under the Installation device

	Manage IoT Open from Home Assistant

The integration exposes HA services that let you perform platform maintenance directly from Home Assistant:

•	Create DeviceX

•	Delete DeviceX

•	Create FunctionX

•	Delete FunctionX

•	Assign FunctionX → DeviceX via meta.device_id

•	Set metadata on both DeviceX and FunctionX (name, unit, icon, public, etc.)

This makes it possible to automate IoT Open management using HA automations and scripts.

 Requirements

•	Home Assistant 2023.12+

•	Python environment provided by Home Assistant

•	IoT Open / Lynx account with:

•	Access to an installation

•	Valid API key (X-API-Key) with read/write permissions
(DeviceX, FunctionX, Status API)

 Installation

1. File Layout

Place the integration into your Home Assistant configuration folder:

<config>/
  custom_components/
    iotopen/
      __init__.py
      manifest.json
      const.py
      api.py
      coordinator.py
      sensor.py
      config_flow.py
      services.yaml
      translations/
        en.json
        sv.json
        de.json
        fr.json
        ar.json

2. Restart Home Assistant

After copying the folder, restart Home Assistant.

3. Add the Integration

In Home Assistant:

Settings → Devices & Services → Add Integration → IoT Open


Enter:

Base URL

Installation ID

API Key

Home Assistant will now automatically discover all FunctionX items and create entities.

 Contributing

Contributions, improvements, and suggestions are welcome!
Feel free to open issues or submit pull requests.

License

This project is available under the MIT License.
See the LICENSE file for details.
