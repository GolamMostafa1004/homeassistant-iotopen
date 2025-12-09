IoT Open – Home Assistant Integration

This repository provides a custom Home Assistant integration for IoT Open (Lynx).

The integration enables Home Assistant to communicate with an IoT Open installation via the REST API and provides full management control of DeviceX and FunctionX, following standard Home Assistant design patterns such as config_flow, DataUpdateCoordinator, translations, and service definitions.

Overview

This integration makes it possible to:

Connect a Lynx installation to Home Assistant through the REST API.

Automatically discover FunctionX objects and expose them as Home Assistant entities.

Retrieve live values using the Status API (topic_read).

Manage DeviceX and FunctionX directly from Home Assistant:

Create, delete, and modify devices and functions.

Assign functions to devices using meta.device_id.

Set metadata (names, units, icons, public visibility, and custom fields).

Data Model

Installation
One Home Assistant config entry corresponds to one IoT Open installation.

DeviceX
Represents a physical device in IoT Open (e.g., controllers, KNX gateways, sensor hubs).

FunctionX
Represents logical datapoints such as temperature, humidity, boolean states, switches, or other measured values.

Status API
Provides the latest status values for all functions that define a topic_read.

How the Integration Works

The integration communicates with IoT Open API v2 over HTTPS using an X-API-Key.
It periodically performs the following operations:

Retrieves all FunctionX objects for the installation.

Reads meta.topic_read for each function.

Fetches the latest status samples from the Status API.

Creates or updates Home Assistant entities based on function types.

Organizes entities under devices:

If meta.device_id is set → entities are grouped under the corresponding DeviceX.

Otherwise → entities are grouped under the installation-level device.

Platform Management from Home Assistant

The integration exposes multiple Home Assistant services to manage IoT Open resources:

Create or delete DeviceX.

Create or delete FunctionX.

Assign a FunctionX to a DeviceX (meta.device_id).

Modify metadata for DeviceX or FunctionX (name, unit, icon, visibility, and custom metadata fields).

These capabilities can be automated using Home Assistant automations or scripts.

Requirements

Home Assistant 2023.12 or newer.

Python environment provided by Home Assistant (no manual dependencies).

An IoT Open / Lynx account with:

Access to an installation.

A valid API key (X-API-Key) with read/write permissions for:

DeviceX

FunctionX

Status API

Installation
1. File Layout

Place the integration in your Home Assistant configuration directory:

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

Restart Home Assistant to ensure the integration is loaded.

3. Add the Integration

Navigate to:

Settings → Devices & Services → Add Integration → IoT Open


Enter the Base URL, Installation ID, and API Key.
Entities will be discovered and created automatically.

Contributing

Contributions are welcome.
You may submit feature requests, issues, or pull requests to improve and expand the integration.

License

This project is licensed under the MIT License.
For details, see the LICENSE file.
