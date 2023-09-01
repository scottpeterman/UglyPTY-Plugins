import os
import sys
from time import time

import yaml
from PyQt6 import QtGui
from PyQt6.QtCore import QProcess
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QFormLayout, \
    QFileDialog, QTextEdit, QComboBox, QCheckBox


def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)

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
        self.selected_file_path = None
        self.argument_metadata = {}

    def choose_script(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Select Click Script", "", "Python Files (*.py);;All Files (*)")
        if filePath:
            self.selected_file_path = filePath  # Store the selected path
            self.try_load_metadata()

    def try_load_metadata(self):
        script_name, _ = os.path.splitext(self.selected_file_path)
        metadata_file_path = script_name + '.yaml'

        if os.path.exists(metadata_file_path):
            self.load_metadata(metadata_file_path)
        else:
            self.load_default_form()

    def load_metadata(self, metadata_file):
        try:
            with open(metadata_file, 'r') as f:
                self.argument_metadata = yaml.safe_load(f)['arguments']

            for arg_name, arg_info in self.argument_metadata.items():
                label = QLabel(arg_name.replace('-', ' ').title())
                widget = None

                if 'choices' in arg_info:
                    widget = QComboBox()
                    widget.addItems(arg_info['choices'])
                elif arg_info.get('type') == 'bool':
                    widget = QCheckBox()
                else:
                    widget = QLineEdit()

                self.formLayout.addRow(label, widget)
                self.set_default_value(widget, arg_info)

            self.run_button.setEnabled(True)
        except Exception as e:
            print(e)

    def set_default_value(self, widget, arg_info):
        if 'default' in arg_info:
            default_value = arg_info['default']
            if isinstance(widget, QLineEdit):
                widget.setText(str(default_value))
            elif isinstance(widget, QComboBox):
                index = widget.findText(str(default_value))
                if index != -1:
                    widget.setCurrentIndex(index)
            elif isinstance(widget, QCheckBox):
                widget.setChecked(default_value)

    def load_default_form(self):
        for arg_name in ['max-job-size', 'yaml-file', 'include', 'exclude', 'netmiko-type', 'output-dir', 'command',
                         'user']:
            label = QLabel(arg_name.replace('-', ' ').title())
            line_edit = QLineEdit()
            self.formLayout.addRow(label, line_edit)

    def run(self):
        collected_args = {}
        for i in range(self.formLayout.rowCount()):
            label = self.formLayout.itemAt(i, QFormLayout.ItemRole.LabelRole).widget()
            widget = self.formLayout.itemAt(i, QFormLayout.ItemRole.FieldRole).widget()
            if label and widget:
                arg_name = label.text().replace(" ", "-").lower()
                arg_value = widget.text() if isinstance(widget, QLineEdit) or isinstance(widget,
                                                                                         QComboBox) else widget.isChecked()
                collected_args[arg_name] = arg_value

        cmd = [self.selected_file_path] + [f'--{k}={v}' for k, v in collected_args.items()]
        self.command_display.setText(' '.join(cmd))
        # ... The rest of your run button code ...

    def run(self):
        try:
            self.start_time = time()
            collected_args = {}
            for i in range(self.formLayout.rowCount()):
                label = self.formLayout.itemAt(i, QFormLayout.ItemRole.LabelRole).widget()
                line_edit = self.formLayout.itemAt(i, QFormLayout.ItemRole.FieldRole).widget()
                if label and line_edit:
                    arg_name = label.text().replace("_", "-")
                    arg_value = line_edit.text()
                    collected_args[arg_name] = arg_value
        except Exception as e:
            print(e)

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



if __name__ == '__main__':
    app = QApplication([])
    window = ClickCommandWidget()
    window.show()
    app.exec()
