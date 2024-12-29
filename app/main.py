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

        # Handle the "echo" command with redirection
        elif command.startswith("echo"):
            if ">" in command:
                parts = shlex.split(command)
                if ">" in parts or "1>" in parts:
                    # Handle redirection
                    operator_index = parts.index(">") if ">" in parts else parts.index("1>")
                    echo_text = " ".join(parts[1:operator_index])
                    output_file = parts[operator_index + 1]
                    with open(output_file, "w") as f:
                        f.write(echo_text + "\n")
            else:
                # Handle normal echo
                cmd = command[5:].strip()
                parts = shlex.split(cmd)
                sys.stdout.write(" ".join(parts) + "\n")
            continue

        # Handle the "pwd" command
        elif command.startswith("pwd"):
            sys.stdout.write(f"{os.getcwd()}\n")
            continue

        # Handle the "type" command
        elif command.startswith("type"):
            cmd = command.split(" ", 1)[1]  # Extract the command name
            builtins = {"cd", "pwd", "echo", "exit", "type"}
            if cmd in builtins:
                sys.stdout.write(f"{cmd} is a shell builtin\n")
                continue

            PATH = os.environ.get("PATH")
            paths = PATH.split(":")
            for path in paths:
                if os.path.isfile(f"{path}/{cmd}"):
                    command_path = f"{path}/{cmd}"
                    sys.stdout.write(f"{cmd} is {command_path}\n")
                    break
            else:
                sys.stdout.write(f"{cmd}: not found\n")
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

        # Handle output redirection for general commands
        if ">" in command or "1>" in command:
            parts = shlex.split(command)
            if ">" in parts or "1>" in parts:
                operator_index = parts.index(">") if ">" in parts else parts.index("1>")
                cmd = parts[:operator_index]
                output_file = parts[operator_index + 1]

                executable_path = findexecutable(cmd[0])
                if executable_path:
                    with open(output_file, "w") as f:
                        try:
                            subprocess.run(cmd, stdout=f, stderr=sys.stderr)
                        except FileNotFoundError:
                            sys.stdout.write(f"{cmd[0]}: command not found\n")
                else:
                    sys.stdout.write(f"{cmd[0]}: command not found\n")
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
