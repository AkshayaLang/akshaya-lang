"""
reader.py — SourceLoader for AkshayaLang Scripts
"""

class SourceLoader:
    def __init__(self, filepath=None, source_string=None):
        self.filepath = filepath
        self.lines = []

        if filepath:
            self._load_from_file()
        elif source_string:
            self._load_from_string(source_string)

    def _load_from_file(self):
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.lines = f.readlines()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.filepath}")
        except Exception as e:
            raise RuntimeError(f"Error reading file {self.filepath}: {str(e)}")

    def _load_from_string(self, source_string):
        self.lines = source_string.splitlines(keepends=True)

    def get_content(self):
        return ''.join(self.lines)

    def get_lines(self):
        return self.lines

    def get_line(self, line_number):
        if 0 <= line_number < len(self.lines):
            return self.lines[line_number]
        return None
