# UglyPTY Plugins

This directory is dedicated to managing and registering plugins for the UglyPTY application. Plugins are Python packages that are distributed as `.whl` (Wheel) files.

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

<div align="center">
  <img src="https://github.com/scottpeterman/UglyPTY/blob/main/screen_shots/uglydark.PNG" alt="UglyPTY Dark" width="400px">
  <hr><img src="https://github.com/scottpeterman/UglyPTY/blob/main/screen_shots/uglylight.png" alt="UglyPTY Light Splash" width="400px">
  <hr><img src="https://github.com/scottpeterman/UglyPTY/blob/main/screen_shots/darklight.png" alt="UglyPTY darklight" width="400px">
  <hr><img src="https://github.com/scottpeterman/UglyPTY/blob/main/screen_shots/lightdark.png" alt="UglyPTY Lightdark" width="400px">
</div>

## Download More Plugins

You can download more `.whl` plugins from [github](https://github.com/scottpeterman/UglyPTY-Plugins).
You can download more `.whl` plugins from [wheels](https://github.com/scottpeterman/UglyPTY-Plugins/tree/main/wheels).

---

For more details or support, visit our [documentation](#).
