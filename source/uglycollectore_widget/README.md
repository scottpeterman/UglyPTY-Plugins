# Network Device Command Collector

## Description

This project is designed to run specific commands on network devices and collect their output. It's an ideal tool for network administrators who want to automate the process of gathering data from multiple network devices. The credentials used for connecting to the network devices are sourced from the same database as UglyPTY session files, with encrypted passwords. The collected data can be used for search and audit functions, as well as drive other automation.

## Features

- Supports standard Netmiko device types (`cisco_xe`, `arista_eos`, `junos` etc).
- Commands and credentials are configurable.
- Saves the output in both clear text and YAML format for easier processing.

### Sample YAML Format

Here is a sample of how the output is stored in YAML format:

```yaml
device:
  command: show cdp nei det
  credsid: 1
  device_type: cisco_ios
  display_name: lan-sw-01
  folder_name: branch1
  host: 10.128.1.10
  timestamp: 2023-08-07 09:07
  username: rtradmin
output: "-------------------------\nDevice ID:..."
status: success
```

## Usage

1. Check the output directory for the gathered data. The default is `Capture`, but you will want to store results by catagory, as all files are named `device_name.yaml`. 

    Sample Folder Structure:
    ```plaintext
   C:.
    └───Sweep
        ├───aruba-cdp
        │   └───text_output
        ├───aruba-lldp
        │   └───text_output
        ├───cdp
        │   └───text_output
        ├───configs
        │   └───text_output
        ├───inventory
        │   └───text_output
        ├───ip_protocol
        │   └───text_output
        └───version
            └───text_output
   ```
## Security

Credentials are securely stored, encrypted in the same database as UglyPTY session files.

## Dependencies

- Python 3.x
- PyYAML
- Netmiko
- PyQt6


## License

This project is licensed under the GPLv3 License. See the `LICENSE.md` file for details.
