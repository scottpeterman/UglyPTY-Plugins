# Cisco Configuration Templating and Parsing with Jinja2 and TTP

This repository provides examples and guidelines for using Jinja2 templates for Cisco device configurations and Text Template Parser (TTP) for parsing Cisco CLI outputs.

## Table of Contents

1. [Jinja2 for Configuration Templating](#jinja2-for-configuration-templating)
2. [TTP for Parsing `show cdp neighbors` Output](#ttp-for-parsing-show-cdp-neighbors-output)

---

## Jinja2 for Configuration Templating

Jinja2 is a modern and designer-friendly templating engine for Python. It is particularly useful for generating network device configurations. This section will demonstrate how to use Jinja2 for automating the configuration of Cisco devices.

### Example:

Suppose you have a configuration requirement for multiple Cisco devices that includes:

- Setting the hostname
- Configuring an IP address on an interface
- Enabling an OSPF process

#### Jinja2 Template

```jinja2
hostname {{ hostname }}
!
interface {{ interface }}
 ip address {{ ip_address }} {{ subnet_mask }}
 no shutdown
!
router ospf {{ ospf_process_id }}
 network {{ network }} area {{ ospf_area }}
```

#### Variables File (YAML)

```yaml
hostname: "Router1"
interface: "GigabitEthernet0/0"
ip_address: "192.168.1.1"
subnet_mask: "255.255.255.0"
ospf_process_id: 1
network: "192.168.1.0"
ospf_area: 0
```

### How to Use:

1. Copy the Jinja2 template into the "Template" text area.
2. Paste the variables from the YAML file into the "Variables" text area.
3. Select "Jinja2" from the mode dropdown.
4. Click "Render" to see the generated Cisco configuration.

---

## Using TTP for Parsing `show cdp neighbors` Output

Text Template Parser (TTP) is a Python library designed to extract data from semi-structured text documents, such as CLI command outputs. This section will demonstrate how to use TTP to parse the output of the `show cdp neighbors` command on a Cisco device.

### Example:

Suppose you have the following sample output of the `show cdp neighbors` command:

#### Sample `show cdp neighbors` Output

```text
Device ID         Local Intrfce       Holdtme    Capability  Platform  Port ID
Router1           Eth 0/1             150        R S I       CISCO    Eth 0/0
Switch1           Eth 0/2             154        S I         WS-C2960 Eth 0/1
```

#### TTP Template

```text
Device ID         Local Intrfce       Holdtme    Capability  Platform  Port ID
{{ hostname | re("(\S+)") }}  {{ local_interface | re("(\S+)") }}  {{ hold_time | re("(\d+)") }}  {{ capability | re("(\S+)") }}  {{ platform | re("(\S+)") }}  {{ port_id | re("(\S+)") }}
```

#### Resulting Parsed Data (JSON)

```json
[
  {
    "hostname": "Router1",
    "local_interface": "Eth 0/1",
    "hold_time": "150",
    "capability": "R S I",
    "platform": "CISCO",
    "port_id": "Eth 0/0"
  },
  {
    "hostname": "Switch1",
    "local_interface": "Eth 0/2",
    "hold_time": "154",
    "capability": "S I",
    "platform": "WS-C2960",
    "port_id": "Eth 0/1"
  }
]
```

### How to Use:

1. Copy the TTP template into the "Template" text area.
2. Paste the `show cdp neighbors` output into the "Source" text area.
3. Select "TTP" from the mode dropdown.
4. Click "Render" to see the parsed data in JSON format.

---
