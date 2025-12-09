IoT Open – Home Assistant Integration

This repository contains a custom Home Assistant integration for IoT Open (Lynx).
It enables Home Assistant to interact with an IoT Open installation through the REST API and provides tools for managing DeviceX and FunctionX directly from Home Assistant.

The integration follows standard Home Assistant development patterns, including config_flow, DataUpdateCoordinator, translations, and service implementations.

Overview

This integration allows you to:

Connect a Lynx installation to Home Assistant via the REST API.

Automatically discover FunctionX objects and represent them as Home Assistant entities.

Retrieve live values using the Status API (topic_read).

Manage DeviceX and FunctionX from Home Assistant.

Create, delete, and modify devices and functions.

Assign functions to devices using meta.device_id.

Set metadata such as names, units, icons, and public visibility.

Data Model

Installation: One Home Assistant config entry corresponds to one IoT Open installation.

DeviceX: Represents physical devices in IoT Open (for example, controllers, KNX gateways, sensor hubs).

FunctionX: Represents logical datapoints (such as temperature, humidity, switches, booleans, and other measured or state values).

Status API: Used to retrieve up-to-date readings for all functions with topic_read defined.

How the Integration Works

The integration uses IoT Open API v2 over HTTPS with an X-API-Key for authentication.
It periodically performs the following actions:

Retrieves all FunctionX objects for the configured installation.

Collects meta.topic_read values for each function.

Fetches the latest available status samples.

Creates or updates Home Assistant entities based on the function type.

Organizes entities under devices:

If meta.device_id is set, entities are grouped under the corresponding DeviceX.

Otherwise, they are grouped under the installation-level device.

Platform Management from Home Assistant

The integration exposes several Home Assistant services that allow management of IoT Open resources:

Create or delete DeviceX.

Create or delete FunctionX.

Assign FunctionX to DeviceX via meta.device_id.

Modify metadata for both DeviceX and FunctionX (e.g., name, unit, icon, public visibility, and custom metadata fields).

These operations can be automated through scripts or automations within Home Assistant.

Requirements

Home Assistant version 2023.12 or newer.

Python environment as provided by Home Assistant (no additional installations required).

An IoT Open/Lynx account with:

Access to a valid installation.

An API key (X-API-Key) with read and write access to DeviceX, FunctionX, and the Status API.

Installation
File Layout

Place the integration under your Home Assistant configuration directory:

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

Restart Home Assistant

Restart Home Assistant to load the integration.

Add the Integration

Navigate to:

Settings → Devices & Services → Add Integration → IoT Open


Enter the Base URL, Installation ID, and API Key for your IoT Open installation.

Entities will be discovered and created automatically.

Contributing

Contributions are welcome.
Please feel free to submit issues, feature requests, or pull requests to improve this integration.

License

This project is licensed under the MIT License.
See the LICENSE file for details.
