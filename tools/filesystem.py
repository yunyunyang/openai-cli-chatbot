import shlex
import subprocess

from pathlib import Path

tools = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a specified file",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string", "description": "File path"}},
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a specified file (overwrites existing content)",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"},
                    "content": {"type": "string", "description": "Content to write"},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Execute a shell command and return the output",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Command to execute"}
                },
                "required": ["command"],
            },
        },
    },
]


BASE_DIR = Path.cwd()

ALLOWED_COMMANDS = ["ls", "pwd", "whoami", "echo", "cat"]


def read_file(path):
    full_path = Path(path).resolve()

    if BASE_DIR not in full_path.parents and full_path != BASE_DIR:
        return "Blocked"

    try:
        with open(full_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File {full_path} does not exist"


def write_file(path, content):
    full_path = Path(path).resolve()

    if BASE_DIR not in full_path.parents and full_path != BASE_DIR:
        return "Blocked"

    with open(full_path, "w") as f:
        f.write(content)

    return f"Written to {full_path}"


def run_command(command):
    try:
        cmd = shlex.split(command)

        if not cmd:
            return "Empty command"

        if cmd[0] not in ALLOWED_COMMANDS:
            return f"Blocked command: {cmd[0]}"

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        output = result.stdout

        # Shell convention: exit code 0 indicates success, non-zero indicates an error
        if result.returncode != 0:
            output += f"\n[Error] {result.stderr}"

        return output or "(No output)"

    except subprocess.TimeoutExpired:
        return "[Error] Command execution timed out (10 seconds)"


tool_functions = {
    "read_file": read_file,
    "write_file": write_file,
    "run_command": run_command,
}
