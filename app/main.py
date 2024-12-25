import sys


def main():
    sys.stdout.write("$ ")
    command = input()
    while command:    
        if command == "exit 0":
            sys.exit(0)
            
        elif command.startswith("echo"):
            sys.stdout.write(command[5:])
            sys.stdout.write("\n$ ")
        else:
            sys.stdout.write(f"{command} : command not found")
            sys.stdout.write("\n$ ")
        

    
if __name__ == "__main__":
    main()
