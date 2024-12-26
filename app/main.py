import sys
import os

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        command = input()
        if not command.strip():
            continue  # Skip empty commands
        
        if command == "exit 0":
            sys.exit(0)

        elif command.startswith("echo"):
            sys.stdout.write(command[5:] + "\n")
            continue

        # Extract the command after "type"
        if command.startswith("type"):
            cmd = command.split(" ", 1)[1]  # Extract the command name
            
            # Check if it is a shell built-in
            builtins = ["cd", "pwd", "echo", "exit", "type"]
            if cmd in builtins:
                sys.stdout.write(f"{cmd} is a shell builtin\n")
                continue

            # Check if the file exists in the PATH
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

        # For unknown commands, print "not found"
        sys.stdout.write(f"{command}: command not found\n")

if __name__ == "__main__":
    main()
