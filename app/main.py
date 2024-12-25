import sys
import os 


def main():
    builtins = ["exit", "echo", "type"]
    PATH = os.environ.get("PATH")
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        command = input() 
        command_path = None
        paths = PATH.split(":")
        for path in paths:
            if os.path.exists(f"{path}/{command}"):
                command_path = f"{path}/{command}"
        #print(paths)        
            
        if command == "exit 0":
            sys.exit(0)
            
        elif command.startswith("echo"):
            sys.stdout.write(command[5:] + "\n") 

        # elif command.startswith("type"):
        #     if command[5:] in builtins:
        #         sys.stdout.write(f"{command[5:]} is a shell builtin\n")
            # else:
            #     sys.stdout.write(f"{command[5:]}: not found\n")   

        elif command_path:
            if command in command_path:
                sys.stdout.write(f"{command} is {command_path}\n")
            else:
                sys.stdout.write(f"{command}: not found\n")
            
        # else:
        #     sys.stdout.write(f"{command}: command not found\n")
            
        

    
if __name__ == "__main__":
    main()
