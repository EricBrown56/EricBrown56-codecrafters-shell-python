import sys
import os
import subprocess
import shlex

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
            
        
        elif command.startswith("echo"):
            if command.startswith("'") or command.startswith('"') and command.endswith("'") or command.endswith('"'):
                sys.stdout.write(f"{command[6:-1]}\n")
            else:
                parts = shlex.split(command[5:])
                sys.stdout.write(" ".join(parts) + "\n")
            continue

        elif command.startswith("pwd"):
            sys.stdout.write(f"{os.getcwd()}\n")
            continue

        # Extract the command after "type"
        if command.startswith("type"):
            cmd = command.split(" ", 1)[1]  # Extract the command name
            
            # Check if it is a shell built-in
            builtins = {"cd", "pwd", "echo", "exit", "type"}
            if cmd in builtins:
                sys.stdout.write(f"{cmd} is a shell builtin\n")
                continue

            # Check if the file exists in the PATH
            PATH = os.environ.get("PATH")
           
            # Split the PATH into individual directories
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
        if command.startswith("cd"):
            try:
                
                target_dir = command.split()[1] if len(command.split()) > 1 else "~"

                # Handle "cd ~"
                if target_dir == "~":
                    target_dir = os.path.expanduser("~")

                # Change to the specified directory
                os.chdir(target_dir)
            except FileNotFoundError:
                sys.stdout.write(f"cd: {command.split()[1]}: No such file or directory\n")
            continue

        # Handle running commands

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
