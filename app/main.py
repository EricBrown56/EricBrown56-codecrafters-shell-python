import sys


def main():
    builtins = ["exit", "echo", "type"]
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        command = input() 
            
        if command == "exit 0":
            sys.exit(0)
            
        elif command.startswith("echo"):
            sys.stdout.write(command[5:] + "\n") 

        elif command.startswith("type"):
            if command[5:] in builtins:
                sys.stdout.write(f"{command[5:]} is a shell builtin\n")
            else:
                sys.stdout.write(f"{command[5:]}: not found\n")    
            
        else:
            sys.stdout.write(f"{command}: command not found\n")
            
        

    
if __name__ == "__main__":
    main()
