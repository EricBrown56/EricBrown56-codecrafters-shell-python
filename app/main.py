import sys


def main():
    
    command = input()
    while command:  
        sys.stdout.write("$ ")  
        if command == "exit 0":
            sys.exit(0)
            break
        elif command.startswith("echo"):
            sys.stdout.write(command[5:])
            continue
        else:
            sys.stdout.write(f"{command} : command not found")
            break
        

    
if __name__ == "__main__":
    main()
