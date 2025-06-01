import sys
import re

class AksInterpreter:
    def __init__(self):
        self.memory = {}
        self.emotions = {}
        self.capsules = {}
        self.current_block = []
        self.current_emotion = None
        self.in_capsule_block = False
        self.emotion_blocks = {}

    def parse_line(self, line):
        line = line.strip()
        if not line or line.startswith(";;"):
            return

        if line.startswith("#emotion("):
            match = re.match(r"#emotion\((.*?)\):", line)
            if match:
                self.current_emotion = match.group(1)
                self.emotion_blocks[self.current_emotion] = []
                return

        elif line.startswith("capsule"):
            self.in_capsule_block = True
            self.current_block = []
            return

        elif line.startswith("mirror") or line.startswith("capsule"):
            self.current_block = []
            return

        elif line == "{":
            self.current_block = []
            return

        elif line == "}":
            if self.current_emotion:
                self.emotion_blocks[self.current_emotion].extend(self.current_block)
                print(f"[emotion block] {self.current_emotion} → {len(self.current_block)} lines")
                self.current_emotion = None
            elif self.in_capsule_block:
                for entry in self.current_block:
                    match = re.match(r"let\s+(\w+)\s*=\s*(.+)", entry)
                    if match:
                        key = match.group(1)
                        value = match.group(2).strip()
                        self.capsules[key] = value
                print(f"[capsule block] → {len(self.current_block)} entries stored")
                self.in_capsule_block = False
            else:
                self.memory["last_block"] = self.current_block
            return

        match = re.match(r"let\s+(\w+)\s*=\s*(.+)", line)
        if match:
            key = match.group(1)
            value = match.group(2).strip()
            if self.current_emotion:
                self.emotion_blocks[self.current_emotion].append(line)
            elif self.in_capsule_block:
                self.current_block.append(line)
            else:
                self.memory[key] = value
                print(f"[let] {key} = {value}")
            return

        match = re.match(r"signal\s+(\w+)\s*->\s*(.+)", line)
        if match:
            action = match.group(1)
            target = match.group(2)
            print(f"[signal] {action} → {target}")
            return

        if self.current_emotion or self.in_capsule_block:
            self.current_block.append(line)

    def run(self, filepath):
        print(f"[run] Executing: {filepath}")
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                self.parse_line(line)

        print("\n[🔮 Execution Complete]")
        print("[📦 Memory State]", self.memory)
        print("[💓 Emotions]", self.emotion_blocks.keys())
        print("[🔐 Capsules]", self.capsules)

if __name__ == "__main__":
    filepath = sys.argv[1] if len(sys.argv) > 1 else "examples/mirror_state.aks"
    interpreter = AksInterpreter()
    interpreter.run(filepath)