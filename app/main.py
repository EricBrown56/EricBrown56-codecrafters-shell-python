import sys


def main():
    sys.stdout.write("$ ")
    command = input()
    while True:
        if command == "exit 0":
            sys.exit(0)
            break
        elif command.startswith("echo"):
            sys.stdout.write(command[5:])
            break
        else:
            sys.stdout.write(f"{command} : command not found")
        sys.stdout.write("$ ")
        

    
if __name__ == "__main__":
    main()
