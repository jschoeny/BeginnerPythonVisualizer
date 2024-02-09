import bdb
import linecache
import re
import runpy
import sys
import traceback
import logging

from PySide6 import QtCore


class StepLogger(bdb.Bdb):
    def __init__(self, parent, main_window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.main_window = main_window
        if main_window:
            self.file_to_visualize = main_window.file_to_visualize
        else:
            self.file_to_visualize = parent.test_file
        self.last_line = None
        self.local_vars = {}
        self.method_params = {}
        with open(self.file_to_visualize) as f:
            self.source = f.readlines()
        self.source_output = self.source.copy()
        self.next_step = False
        self.variable_changed = False
        self.methods_to_update = []
        self.ready = False
        self.quitting = False

    def user_line(self, frame):
        """This method is called when we stop or break at this line."""
        sys.stdout = self.parent.stdout_
        self.next_step = False
        self.variable_changed = False
        self.ready = False

        if self.last_line is not None:
            self.update_var_changes(frame)
            for method_name in self.methods_to_update:
                self.update_method_variables(method_name)
            self.methods_to_update = []
            if self.variable_changed:
                self.parent.emit_line_finished(self.last_line - 1)
            # Wait for user to press Next Line button
            if not self.next_step and self.variable_changed:
                print("Variable Changed: Waiting for user to press Next Line button")
            self.ready = True
            while not self.next_step and self.variable_changed and not self.quitting:
                pass
            self.last_line = None
            self.ready = False
            self.next_step = False
            self.variable_changed = False

        if "__file__" not in frame.f_globals:
            sys.stdout = self.parent.stream_out
            return
        filename = frame.f_globals["__file__"]
        if filename.count(self.file_to_visualize) == 1:
            lineno = frame.f_lineno
            self.last_line = lineno
            line = linecache.getline(filename, lineno).strip()
            print(f"About to execute {filename}:{lineno} - {line}")

            # Wait for user to press Next Line button
            if not self.next_step:
                print("Waiting for user to press Next Line button")
            self.ready = True
            self.parent.emit_line_finished(lineno - 1)
            while not self.next_step and not self.quitting:
                pass
            self.ready = False
            current_line = self.source[lineno - 1]

            # Make sure the line is not a method definition
            if not current_line.strip().startswith("def"):
                # Use regex to check if current line contains method call(s)
                method_names = re.findall(r"\b(\w+)\(", current_line)
                for method_name in method_names:
                    self.methods_to_update.append(method_name)

        sys.stdout = self.parent.stream_out

    def update_method_variables(self, method_name):
        if method_name not in self.method_params:
            return

        # Find line number of `def method_name`
        method_lineno = 0
        for i in range(len(self.source)):
            if self.source[i].strip().startswith("def") and method_name in self.source[i].split():
                method_lineno = i
                break
        method_indent = len(self.source[method_lineno]) - len(self.source[method_lineno].lstrip())

        # Find the end of the method
        method_lineno_end = method_lineno
        for i in range(method_lineno + 1, len(self.source)):
            if len(self.source[i]) - len(self.source[i].lstrip()) <= method_indent and self.source[i].strip() != "":
                method_lineno_end = i
                break

        print(f"Updating variables for method {method_name} from line {method_lineno} to {method_lineno_end}")

        for i in range(method_lineno + 1, method_lineno_end):
            current_line = self.source[i]
            print(f"Updating method variables for line {i + 1}: {current_line.rstrip()}")
            for var, value in self.local_vars.items():
                print(var)
                # Replace any instances of var after any equals sign
                if current_line.strip().startswith("#"):
                    continue
                current_line = re.sub(rf"\b{var}\b", '\u200A' + str(value) + '\u200A', current_line.rstrip())
                if current_line != self.source_output[i].rstrip():
                    print(f"[Method] Changed line {i + 1}: {self.source_output[i].rstrip()} -> {current_line.rstrip()}")
                    self.source_output[i] = current_line + "\n"
                    self.parent.emit_line_updated(i, self.source_output[i])

    def update_var_changes(self, frame):
        """Updates the difference in variable values from the last step."""
        current_vars = frame.f_locals
        # Get the name of the called method up the stack
        method_origin = frame.f_code.co_name
        if method_origin in self.method_params:
            for param in self.method_params[method_origin]:
                if param in current_vars:
                    self.local_vars[param] = current_vars[param]
                    if self.main_window:
                        self.main_window.updateVariable.emit((param, str(current_vars[param])))

        # Remove any variables in self.local_vars that are not in current_vars
        for var in list(self.local_vars.keys()):
            if var not in current_vars:
                self.local_vars.pop(var)
                if self.main_window:
                    self.main_window.updateVariable.emit((var, None))

        just_assigned = []
        for var, value in current_vars.items():
            if type(value) is str:
                value = f"'{value}'"
            if var not in self.local_vars or self.local_vars[var] != value:
                current_line = self.source[self.last_line - 1]
                if current_line.strip().startswith(var):
                    if self.main_window:
                        self.main_window.updateVariable.emit((var, str(value)))
                    leading_whitespace = len(current_line) - len(current_line.lstrip())
                    self.source_output[self.last_line - 1] = f"{leading_whitespace * ' '}{var} = \u200A{value}\u200A\n"
                    print(f"[Source] Changed {var} assignment for line {self.last_line}: "
                                  f"{current_line.rstrip()} -> {self.source_output[self.last_line - 1].rstrip()}")
                    self.parent.emit_line_updated(self.last_line - 1, self.source_output[self.last_line - 1])
                    self.local_vars[var] = value
                    self.variable_changed = True
                    just_assigned.append(var)
                else:
                    # extract parameters from for loop and check if var is one of them
                    if current_line.strip().startswith("for") and "in" in current_line:
                        params = current_line[current_line.index("for") + 3:current_line.index("in")].strip()
                        params = params.split(",")
                        for param in params:
                            if param.strip() == var:
                                if self.main_window:
                                    self.main_window.updateVariable.emit((var, str(value)))
                                self.local_vars[var] = value

        # Find line number of `def method_origin`
        method_lineno = self.last_line - 1
        for i in range(self.last_line - 1, -1, -1):
            if self.source[i].strip().startswith("def") and method_origin in self.source[i].split():
                method_lineno = i + 1
                break

        # source_backup = self.source.copy()
        for i in range(method_lineno, len(self.source)):
            current_line = self.source[i]  # source_backup[i]
            # Replace any instances of var after any equals sign
            if current_line.strip().startswith("#"):
                continue
            for var, value in current_vars.items():
                if var not in self.local_vars:
                    continue
                skip = False
                for v in just_assigned:
                    if current_line.strip().startswith(v):
                        skip = True
                if skip:
                    continue
                if "=" in current_line and current_line.strip().startswith(var):
                    if "==" in current_line:
                        continue
                    assignment = current_line.split("=")
                    if len(assignment) == 2:
                        assignment[1] = re.sub(rf"\b{var}\b", '\u200A' + str(value) + '\u200A', assignment[1].rstrip())
                        print(f"Variable {var} just assigned to {value}!")
                        self.source_output[i] = "=".join(assignment) + "\n"
                        print(f"[Source] Changed {var} assignment for line {i + 1}: "
                                      f"{current_line.rstrip()} -> {"=".join(assignment)}")
                else:
                    match = re.search(rf"\b{var}\b", current_line)
                    if match is not None:
                        current_line = re.sub(rf"\b{var}\b", '\u200A' + str(value) + '\u200A', current_line.replace('\n', ''))
                        print(f"[Source] Changed {var} for line {i + 1}: {self.source_output[i].rstrip()} -> {current_line}")
                        self.source_output[i] = current_line + "\n"
                        self.parent.emit_line_updated(i, self.source_output[i])

        # Extract parameters from def function and check if var is one of them
        current_line = self.source[self.last_line - 1]
        if current_line.strip().startswith("def") and "(" in current_line and ")" in current_line:
            method_name = current_line[current_line.index("def") + 3:current_line.index("(")].strip()
            params = current_line[current_line.index("(") + 1:current_line.index(")")]
            params = params.split(",")
            self.method_params[method_name] = params

        lineno = -1
        if self.variable_changed:
            lineno = self.last_line - 1
        elif "__file__" in frame.f_globals:
            filename = frame.f_globals["__file__"]
            if filename.count(self.file_to_visualize) == 1:
                lineno = frame.f_lineno - 1
        self.parent.emit_go_to_line(lineno)


class StepLoggerThread(QtCore.QThread):
    error = QtCore.Signal(tuple)

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        if main_window:
            self.line_updated_signal = main_window.lineUpdated
            self.go_to_line_signal = main_window.goToLine
            self.line_finished_signal = main_window.lineFinished
            self.stream_out = EmittingStream(self.main_window.stdout)
        else:
            self.line_updated_signal = None
            self.go_to_line_signal = None
            self.line_finished_signal = None
            self.stream_out = sys.stdout
        self.step_logger: StepLogger | None = None
        self.wait = False
        self.stdout_ = sys.stdout
        self.test_file = None

    def run(self):
        self.step_logger = StepLogger(self, self.main_window)
        try:
            self.step_logger.set_trace()
            if self.main_window:
                print(f"Running {self.main_window.file_to_visualize}")
                sys.stdout = self.stream_out
                runpy.run_path(self.main_window.file_to_visualize, run_name="__main__")
                sys.stdout = self.stdout_
            elif self.test_file:
                runpy.run_path(self.test_file, run_name="__main__")
        except bdb.BdbQuit:
            pass
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.stop()

    def stop(self):
        sys.stdout = self.stdout_
        if self.step_logger is not None:
            self.step_logger.set_quit()
            self.next_step()
        self.emit_line_updated(-1, "")
        self.quit()

    def next_step(self) -> tuple[int, str] | tuple[None, None]:
        if not self.step_logger:
            return None, None
        while not self.step_logger.ready and not self.step_logger.quitting:
            pass
        self.step_logger.ready = False
        self.step_logger.next_step = True
        if self.step_logger.last_line is None:
            return None, None
        return self.step_logger.last_line - 1, self.step_logger.source_output[self.step_logger.last_line - 1]
        
    def emit_line_updated(self, lineno, line):
        if self.line_updated_signal:
            self.line_updated_signal.emit(lineno, line)
        
    def emit_go_to_line(self, lineno):
        if self.go_to_line_signal:
            self.go_to_line_signal.emit(lineno)
        
    def emit_line_finished(self, lineno):
        if self.line_finished_signal:
            self.line_finished_signal.emit(lineno)

    def emit_ready(self):
        if self.line_finished_signal:
            self.line_finished_signal.emit(-1)
        
    def set_test_file(self, test_file):
        self.test_file = test_file
        self.stream_out = None


class EmittingStream(QtCore.QObject):

    def __init__(self, signal):
        super().__init__()
        self.stdout = signal

    def write(self, text):
        self.stdout.emit(str(text))

    def flush(self):
        pass
