import os
import sys
from time import time

from PyQt6 import QtGui
from PyQt6.QtCore import QThread, pyqtSignal, QProcess
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QFormLayout, \
    QFileDialog, QPlainTextEdit, QTextEdit
import importlib.util
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)


class ExecuteScriptThread(QThread):
    output_received = pyqtSignal(str)

    def __init__(self, command):
        super(ExecuteScriptThread, self).__init__()
        self.command = command

class ClickCommandWidget(QWidget):
    def __init__(self, parent=None):
        super(ClickCommandWidget, self).__init__(parent)
        self.p = None
        self.layout = QVBoxLayout()
        self.setMinimumWidth(600)
        self.setMinimumHeight(600)

        self.choose_script_button = QPushButton("Choose Click Script")
        self.choose_script_button.clicked.connect(self.choose_script)
        self.layout.addWidget(self.choose_script_button)

        self.formLayout = QFormLayout()
        self.layout.addLayout(self.formLayout)

        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(self.run)
        self.layout.addWidget(self.run_button)
        self.run_button.setEnabled(False)
        self.command_display = QLineEdit()
        self.command_display.setReadOnly(True)
        self.layout.addWidget(self.command_display)
        self.output_edit = QTextEdit()
        self.layout.addWidget(self.output_edit)

        self.setLayout(self.layout)
        self.execute_thread = None

    def choose_script(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Select Click Script", "", "Python Files (*.py);;All Files (*)")
        if filePath:
            self.selected_file_path = filePath  # Store the selected path
            self.params = self.import_click_command(filePath)
            for param in self.params:
                param_name = param.get('name')
                param_help = param.get('help')
                param_default = param.get('default')

                label = QLabel(param_name)
                line_edit = QLineEdit()
                if param_help:
                    line_edit.setToolTip(param_help)
                if param_default is not None:
                    line_edit.setText(str(param_default))
                self.formLayout.addRow(label, line_edit)
            self.run_button.setEnabled(True)

    def run(self):
        self.start_time = time()
        collected_args = {}
        for i in range(self.formLayout.rowCount()):
            label = self.formLayout.itemAt(i, QFormLayout.ItemRole.LabelRole).widget()
            line_edit = self.formLayout.itemAt(i, QFormLayout.ItemRole.FieldRole).widget()
            if label and line_edit:
                arg_name = label.text().replace("_", "-")
                arg_value = line_edit.text()
                collected_args[arg_name] = arg_value

        cmd = [sys.executable, self.selected_file_path] + [f'--{k}={v}' for k, v in collected_args.items()]
        print(cmd)
        self.command_display.setText(' '.join(cmd))
        if self.p is None:
            self.p = QProcess()
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.readyReadStandardError.connect(self.handle_stderr)
            self.p.stateChanged.connect(self.handle_state)
            self.p.finished.connect(self.process_finished)

            try:
                self.p.start(cmd[0], cmd[1:])
            except Exception as e:
                print(e)

    def stop_process(self):
        self.p.kill()

    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self.message(stderr)

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        # stdout = '<style="line-height: 0.7;">' + stdout + '</style>'
        self.message(stdout)

    def handle_state(self, state):
        states = {
            QProcess.ProcessState.NotRunning: 'Not running',
            QProcess.ProcessState.Starting: 'Starting',
            QProcess.ProcessState.Running: 'Running',
        }
        state_name = states[state]
        self.output_edit.append(f'<h3 style="color:green;">State changed: <font color="grey">{state_name}</font></h3>')

    def process_finished(self):
        duration = convert_seconds(time() - self.start_time)
        self.output_edit.append(f"<h4>Process finished. [{duration}]</h4>")

        self.p = None

    def message(self, s):
        # conv = Ansi2HTMLConverter()

        if True:
            # linetext = conv.convert(s)
            if "[0m" not in s:
                linetext = s
                # print(linetext)
                linetext = linetext.replace("\r", "")
                # linetext = linetext.replace("\n", "")
                linetext = '<pre style="color:grey;">' + linetext + '</pre><br>'
                self.output_edit.append(linetext)
                self.output_edit.moveCursor(QtGui.QTextCursor.MoveOperation.End)


    def import_click_command(self, script_path):
        spec = importlib.util.spec_from_file_location("module.name", script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        main_func = getattr(module, "main", None)

        if main_func and hasattr(main_func, 'params'):
            params = main_func.params
            params_list = []
            for param in params:
                param_dict = {}
                param_dict['name'] = param.name
                param_dict['help'] = param.help
                param_dict['default'] = param.default
                params_list.append(param_dict)

            return params_list
        return []

if __name__ == '__main__':
    app = QApplication([])
    window = ClickCommandWidget()
    window.show()
    app.exec()