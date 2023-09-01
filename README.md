# UglyPTY Plugins

This directory is dedicated to managing and registering plugins for the UglyPTY application. Plugins are Python packages that are distributed as `.whl` (Wheel) files. Some of them are purly standalone functionality. Others benefit from UglyPTY's base functionality.

## Why?

The whole point of the UglyPTY project is not to solve every problem, but to provide a platform based on the tool network engineers use most - an SSH Terminal. Developers like text editors with add-on capabilites, this is just the equivilent for CLI focused engineers. Nothing in these plugins is supper special, I just wanted to provide enough examples that others could create there own tools. Both the usable .whl files, as well as original source code are included in the repo. These are all beta tools, be careful ;)


## Getting Started

To use a plugin, download its `.whl` file and save it in the `./wheels` directory where your UglyPTY application is installed.

## `catalog.yaml` Explained

The `catalog.yaml` file contains metadata for all available plugins. Each plugin has its entry defined by the following keys:

- `name`: The human-readable name of the plugin.
- `package_name`: The name used to register the plugin as a Python package. This is the name you would use if you were to install the plugin using pip.
- `description`: A brief description of what the plugin does.
- `import_name`: The Python import statement that would be used to load the plugin's main class or function.
- `version`: The version number of the plugin.
- `source_type`: The type of installation source, currently only supports "wheel".
- `wheel_url`: The path to the `.whl` file for the plugin, relative to the `./wheels` directory.

Example entry:

```yaml
- name: "Ugly Ace Editor"
  package_name: "ugly_ace_editor"
  description: "An Ace based editor with some unique features."
  import_name: "uglyplugin_ace.ugly_ace.QtAceWidget"
  version: "0.1.0"
  source_type: "wheel"
  wheel_url: "./wheels/uglyplugin_ace-0.1.0-py3-none-any.whl"
```

## Database Registration

When you install a plugin through the UglyPTY Plugin Manager, the plugin's metadata is registered in a SQLite database (`settings.SQLite`). This enables the application to keep track of installed plugins and their status.

The following columns are used in the `installed_plugins` table:

- `name`: Same as the `name` in `catalog.yaml`.
- `package_name`: Same as the `package_name` in `catalog.yaml`.
- `description`: Same as the `description` in `catalog.yaml`.
- `import_name`: Same as the `import_name` in `catalog.yaml`.
- `status`: Indicates if the plugin is currently installed.

## Extending the Catalog

You can extend the catalog by simply adding more entries to the `catalog.yaml` file following the format shown above. After updating `catalog.yaml`, you may need to refresh the Plugin Manager UI to see the new entries.

## Screenshots

Here are some snapshots of UglyPTY-Plugins in action:

### Serial Terminal Widget Description

The PyQt6 Serial Terminal Widget provides a terminal interface over a com port. Network Engineers need console cable support!

<div align="center"><img src="https://github.com/scottpeterman/UglyPTY-Plugins/blob/main/screen_shots/serial.png" alt="UglyPTY Serial Console" width="400px"></div>

### Terminal Widget Description

The PyQt6 Windows Terminal Widget provides a terminal interface within a PyQt6 application that can interact with different shells such as cmd, PowerShell, or Windows Subsystem for Linux (WSL2). Users can execute shell commands directly from this widget.

<div align="center"><img src="https://github.com/scottpeterman/UglyPTY-Plugins/blob/main/screen_shots/UglyConsole.png" alt="UglyPTY Console" width="400px"></div>

### Netmiko Threaded GUI Collector Description

This project is designed to run specific commands on network devices and collect their output. It's an ideal tool for network administrators who want to automate the process of gathering data from multiple network devices. The credentials used for connecting to the network devices are sourced from the same database as UglyPTY session files, with encrypted passwords. The collected data can be used for search and audit functions, as well as drive other automation. The CLI output result is stored in both a structured yaml file, and a raw text file. The meta-data in the yaml file can enable autiting, searching or other automations.

 - Example Structured Data
 ```text
 device:
  command: show lldp info remote-device detail
  credsid: 1
  device_type: hp_procurve
  display_name: retail-swl-01
  folder_name: r1
  host: 10.100.10.1
  timestamp: 2023-08-07 11:39
  username: autoadmin
output: "\n\n LLDP Remote Device Information Detail\n\n  Local Port   : 1\n  ChassisType\
  \  : mac-address         \n  ChassisId    : 0010f3-879897            \n  PortType\
  \     : mac-address                                               \n  PortId   \
  \    : 00 10 f3 87 98 97                                         \n  SysName   \
  \   :                                 \n  System Descr :                       \
  \                                      \n  PortDescr    :                      \
  \                                       \n  Pvid         :                     \
  \     \n\n  System Capabilities Supported  : \n  System Capabilities Enabled   \
  \ : \n\n  Remote Management Address\n\n  MED Information Detail \n    EndpointClass\
  \          :Class1\n\n------------------------------------------------------------------------------\n\
  \  Local Port   : 3\n  ChassisType  : mac-address         \n  ChassisId    : 0010f3-8797f3\
  \            \n  PortType     : mac-address                                    \
  \           \n  PortId       : 00 10 f3 87 97 f3                               \
  \          \n  SysName      :                                 \n  System Descr :\
  \                                                             \n  PortDescr    :\
  \                                                             \n  Pvid         :\
  \                          \n\n  System Capabilities Supported  : \n  System Capabilities\
  \ Enabled    : \n\n  Remote Management Address\n\n  MED Information Detail \n  \
  status: success
```

<div align="center"><hr><img src="https://github.com/scottpeterman/UglyPTY-Plugins/blob/main/screen_shots/UglyCollector.png" alt="Netmiko based GUI cli collector for Netmiko" width="400px"></div>

### Device Configuration Templating and Parsing with Jinja2 and TTP with query testing for JMESPath

This plugin is both a test tool, as well as provides examples and guidelines for using Jinja2 templates for Network device configurations and Text Template Parser (TTP) for parsing Network Device CLI outputs.

<div align="center"> <hr><img src="https://github.com/scottpeterman/UglyPTY-Plugins/blob/main/screen_shots/UglyParser.png" alt="TTP, Jinja and JMESPath util" width="400px"></div>

### Click Automated Front End

This plugin loads a Click based cli script. It then renders a dynamic form based on the click parameters and allows the user to run the script and see the results realtime streamed to the GUI. A useful and quick way to put a front end on a script.

<div align="center"><hr><img src="https://github.com/scottpeterman/UglyPTY-Plugins/blob/main/screen_shots/clickfe.png" alt="Front End dynamic forms for click scripts" width="400px"></div>
 


## Download More Plugins

You can download more `.whl` plugins from [github](https://github.com/scottpeterman/UglyPTY-Plugins).
You can download more `.whl` plugins from [wheels](https://github.com/scottpeterman/UglyPTY-Plugins/tree/main/wheels).

---

For more details or support, visit our [documentation](#).
