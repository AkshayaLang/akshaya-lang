# aks/reader.py

class SourceReader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.lines = []
        self._load()

    def _load(self):
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.lines = f.readlines()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.filepath}")
        except Exception as e:
            raise RuntimeError(f"Error reading file {self.filepath}: {str(e)}")

    def get_content(self):
        return ''.join(self.lines)

    def get_lines(self):
        return self.lines

    def get_line(self, line_number):
        if 0 <= line_number < len(self.lines):
            return self.lines[line_number]
        return None