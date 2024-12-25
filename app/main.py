import sys


def main():
    sys.stdout.write("$ ")
    command = input()
    if command == "exit 0":
        sys.exit(0)
    elif command.startswith("echo"):
        sys.stdout.write(command[5:])
        

    
if __name__ == "__main__":
    main()
