import sys
import os
import subprocess
import shlex

def findexecutable(command):
    paths = os.getenv("PATH", "").split(os.pathsep)
    for path in paths:
        executable_path = os.path.join(path, command)
        if os.path.isfile(executable_path):
            return executable_path
    return None

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        command = input().strip()
        if not command:
            continue  # Skip empty commands

        # Handle the "exit" command
        if command == "exit 0":
            sys.exit(0)

        # Handle the "pwd" command
        if command == "pwd":
            sys.stdout.write(f"{os.getcwd()}\n")
            continue

        # Handle the "cd" command
        if command.startswith("cd"):
            parts = shlex.split(command)
            try:
                target_dir = parts[1] if len(parts) > 1 else "~"
                if target_dir == "~":
                    target_dir = os.path.expanduser("~")
                os.chdir(target_dir)
            except FileNotFoundError:
                sys.stdout.write(f"cd: {target_dir}: No such file or directory\n")
            continue

        # Handle the "echo" command with redirection
        elif command.startswith("echo"):
            parts = shlex.split(command)
            stdout_file = None
            stderr_file = None

            # Check for redirection operators
            if ">" in parts or "1>" in parts:
                operator_index = parts.index(">") if ">" in parts else parts.index("1>")
                stdout_file = parts[operator_index + 1]
                parts = parts[:operator_index]
            elif "2>" in parts:
                operator_index = parts.index("2>")
                stderr_file = parts[operator_index + 1]
                parts = parts[:operator_index]

            # Handle output and error redirection
            if stdout_file:
                with open(stdout_file, "w") as f:
                    f.write(" ".join(parts[1:]) + "\n")
            elif stderr_file:
                with open(stderr_file, "w") as f:
                    sys.stderr.write(" ".join(parts[1:]) + "\n")
            else:
                sys.stdout.write(" ".join(parts[1:]) + "\n")
            continue

        # Handle output and error redirection for general commands
        if ">" in command or "1>" in command or "2>" in command:
            parts = shlex.split(command)
            stdout_file = None
            stderr_file = None

            if ">" in parts or "1>" in parts:
                operator_index = parts.index(">") if ">" in parts else parts.index("1>")
                stdout_file = parts[operator_index + 1]
                cmd = parts[:operator_index]

            if "2>" in parts:
                operator_index = parts.index("2>")
                stderr_file = parts[operator_index + 1]
                cmd = parts[:operator_index]

            executable_path = findexecutable(cmd[0])
            if executable_path:
                stdout_f = open(stdout_file, "w") if stdout_file else None
                stderr_f = open(stderr_file, "w") if stderr_file else None
                try:
                    subprocess.run(cmd, stdout=stdout_f, stderr=stderr_f)
                finally:
                    if stdout_f:
                        stdout_f.close()
                    if stderr_f:
                        stderr_f.close()
            else:
                sys.stdout.write(f"{cmd[0]}: command not found\n")
            continue

        # Handle the "type" command
        if command.startswith("type"):
            cmd_name = command.split(" ", 1)[1] if len(command.split()) > 1 else ""
            builtins = {"cd", "pwd", "echo", "exit", "type"}
            if cmd_name in builtins:
                sys.stdout.write(f"{cmd_name} is a shell builtin\n")
            else:
                executable_path = findexecutable(cmd_name)
                if executable_path:
                    sys.stdout.write(f"{cmd_name} is {executable_path}\n")
                else:
                    sys.stdout.write(f"{cmd_name}: not found\n")
            continue

        # Handle running commands
        args = shlex.split(command)
        executable_path = findexecutable(args[0])
        if executable_path:
            try:
                subprocess.run(args)
            except FileNotFoundError:
                sys.stdout.write(f"{args[0]}: command not found\n")
            continue

        PATH = os.environ.get("PATH")
        paths = PATH.split(":")
        for path in paths:
            if os.path.isfile(f"{path}/{command.split()[0]}"):
                os.system(command)
                break
        else:
            sys.stdout.write(f"{command.split()[0]}: command not found\n")
            continue

if __name__ == "__main__":
    main()




