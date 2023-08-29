from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTabWidget, QToolButton, QMessageBox, QInputDialog
import sys
from uglyplugin_terminal.qtwincon_widget import Ui_Terminal


class TerminalsUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(800)
        self.setFixedHeight(600)
        self.layout = QVBoxLayout(self)
        self.tabWidget = QTabWidget(self)
        self.tabWidget.setTabsClosable(True)
        self.addButton = QPushButton(self)
        self.addButton.setText('+')
        self.addButton.setFixedWidth(30)
        self.addButton.clicked.connect(lambda: self.addTerminalTab(shell=None))
        self.layout.addWidget(self.addButton)
        self.layout.addWidget(self.tabWidget)
        self.setWindowTitle("Ugly Consoles")

        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        self.addTerminalTab("cmd.exe")

    def addTerminalTab(self, shell=None):
        try:
            if shell is None:
                items = ("cmd.exe", "powershell.exe", "wsl.exe")
                shell, ok = QInputDialog.getItem(self, "Select a shell", "Shell:", items, 0, False)
                if not ok or not shell:
                    return

            terminal = Ui_Terminal(shell)
            index = self.tabWidget.addTab(terminal, shell)
            self.tabWidget.setCurrentIndex(index)
        except Exception as e:
            print(e)

    def closeTab(self, index):
        try:
            reply = QMessageBox.question(self, 'Confirmation',
                                         "Are you sure you want to close this tab?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                self.tabWidget.removeTab(index)
        except Exception as e:
            print(e)

def main():
    try:
        app = QApplication(sys.argv)
        mainWin = TerminalsUI()
        mainWin.show()
        sys.exit(app.exec())

    except Exception as e:
        print(f"Exception in main: {e}")


if __name__ == "__main__":
    main()
