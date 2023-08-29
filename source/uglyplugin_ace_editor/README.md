# PyQt6 Ace Editor Widget (QtAce_Widget)

This README provides an overview of the PyQt6 Ace Editor Widget (QtAce_Widget), detailing its functionality, dependencies, and usage.

## Overview

The PyQt6 Ace Editor Widget is a code editor widget within a PyQt6 application. It is an implementation of the Ace code editor, allowing users to edit files directly from this widget.

## Dependencies

The PyQt6 Ace Editor Widget is dependent on the following libraries:

- PyQt6
- PyQt6.QtWidgets
- PyQt6.QtGui
- PyQt6.QtCore

In addition, this widget uses a custom module:

- editor: This module provides the implementation of the Ace code editor.

Ensure that all these dependencies are properly installed and available in your environment.

## Additional Notes

The `QtAceWidget` class provides various features, including creating a new file, opening an existing file, saving a file, saving a file with a new name, and exiting the application. These functions are tied to corresponding menu options in the application.

The custom module `editor` should be located in a folder named "Library" at the same level as the `qtace_widget.py` file based on the provided import statements.

For debugging, the script prints instructions for enabling the chrome remote debugger when run. If necessary, the script can be run with the argument `--webEngineArgs --remote-debugging-port=9222` to allow for web engine debugging.

If you wish to customize the icons for the "New", "Open", "Save", "Save As", and "Exit" actions, you can replace the respective PNG files in the "icons" folder. The paths to these icons are provided in the creation of the `QAction` objects within the `createMenus()` method.

The `Editor` class, from the "editor" module, is used to create a code editing interface within the `QtAceWidget` class. This class should include methods to handle the loading, displaying, and saving of file content.

The `QStatusBar` at the bottom of the `QtAceWidget` displays the path of the currently open file.

