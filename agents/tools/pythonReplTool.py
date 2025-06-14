import sys
from io import StringIO
import contextlib

class PythonREPLTool:
    @contextlib.contextmanager
    def capture_output(self):
        new_out = StringIO()
        old_out = sys.stdout
        try:
            sys.stdout = new_out
            yield sys.stdout
        finally:
            sys.stdout = old_out

    def execute(self, code):
        try:
            with self.capture_output() as output:
                exec(code)
            result = output.getvalue()
            return result if result.strip() else "Code executed successfully."
        except Exception as e:
            return f"Python execution error: {str(e)}"