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

def ensure_directory_exists(file_path):
    """Ensure the directory for the given file path exists."""
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

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

        # Handle the "echo" command with redirection and append
        elif command.startswith("echo"):
            parts = shlex.split(command)
            stdout_file = None
            stderr_file = None
            stdout_mode = "w"  # Default to write mode
            stderr_mode = "w"

            # Check for append or redirection operators
            if ">>" in parts or "1>>" in parts:
                operator_index = parts.index(">>") if ">>" in parts else parts.index("1>>")
                stdout_file = parts[operator_index + 1]
                stdout_mode = "a"  # Switch to append mode
                parts = parts[:operator_index]
            elif ">" in parts or "1>" in parts:
                operator_index = parts.index(">") if ">" in parts else parts.index("1>")
                stdout_file = parts[operator_index + 1]
                parts = parts[:operator_index]
            elif "2>>" in parts:
                operator_index = parts.index("2>>")
                stderr_file = parts[operator_index + 1]
                stderr_mode = "a"  # Switch to append mode
                parts = parts[:operator_index]
            elif "2>" in parts:
                operator_index = parts.index("2>")
                stderr_file = parts[operator_index + 1]
                parts = parts[:operator_index]

            # Handle output and error redirection
            if stdout_file:
                ensure_directory_exists(stdout_file)
                with open(stdout_file, stdout_mode) as f:
                    f.write(" ".join(parts[1:]) + "\n")
            elif stderr_file:
                # ensure_directory_exists(stderr_file)
                with open(stderr_file, stderr_mode) as f:
                    f.write(" ".join(parts[1:]) + "\n")
            else:
                sys.stdout.write(" ".join(parts[1:]) + "\n")
            continue

        # Handle the "pwd" command
        elif command == "pwd":
            sys.stdout.write(f"{os.getcwd()}\n")
            continue

        # Handle the "cd" command
        elif command.startswith("cd"):
            try:
                target_dir = command.split()[1] if len(command.split()) > 1 else "~"
                if target_dir == "~":
                    target_dir = os.path.expanduser("~")
                os.chdir(target_dir)
            except FileNotFoundError:
                sys.stdout.write(f"cd: {command.split()[1]}: No such file or directory\n")
            continue

        # Handle the "type" command
        elif command.startswith("type"):
            cmd = command.split(" ", 1)[1]
            builtins = {"cd", "pwd", "echo", "exit", "type"}
            if cmd in builtins:
                sys.stdout.write(f"{cmd} is a shell builtin\n")
            else:
                executable_path = findexecutable(cmd)
                if executable_path:
                    sys.stdout.write(f"{cmd} is {executable_path}\n")
                else:
                    sys.stdout.write(f"{cmd}: not found\n")
            continue

        # Handle general commands with redirection and append
        if ">>" in command or "1>>" in command or "2>>" in command or ">" in command or "2>" in command:
            parts = shlex.split(command)
            stdout_file = None
            stderr_file = None
            stdout_mode = "a" if ">>" in parts or "1>>" in parts else "w"
            stderr_mode = "a" if "2>>" in parts else "w"

            if ">>" in parts or "1>>" in parts:
                operator_index = parts.index(">>") if ">>" in parts else parts.index("1>>")
                stdout_file = parts[operator_index + 1]
                cmd = parts[:operator_index]
            elif ">" in parts or "1>" in parts:
                operator_index = parts.index(">") if ">" in parts else parts.index("1>")
                stdout_file = parts[operator_index + 1]
                cmd = parts[:operator_index]
            if "2>>" in parts:
                operator_index = parts.index("2>>")
                stderr_file = parts[operator_index + 1]
                cmd = parts[:operator_index]
            elif "2>" in parts:
                operator_index = parts.index("2>")
                stderr_file = parts[operator_index + 1]
                cmd = parts[:operator_index]

            executable_path = findexecutable(cmd[0])
            if executable_path:
                if stdout_file:
                    ensure_directory_exists(stdout_file)
                if stderr_file:
                    ensure_directory_exists(stderr_file)

                stdout_f = open(stdout_file, stdout_mode) if stdout_file else None
                stderr_f = open(stderr_file, stderr_mode) if stderr_file else None
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

        # Handle general commands
        args = shlex.split(command)
        executable_path = findexecutable(args[0])
        if executable_path:
            try:
                subprocess.run(args)
            except FileNotFoundError:
                sys.stdout.write(f"{args[0]}: command not found\n")
            continue

        sys.stdout.write(f"{args[0]}: command not found\n")

if __name__ == "__main__":
    main()





