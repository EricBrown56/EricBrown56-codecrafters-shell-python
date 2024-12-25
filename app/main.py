import sys


def main():
    sys.stdout.write("$ ")
    while True:
        command = input()
        if command == "exit 0":
            break
        
        sys.stdout.write("$ ")
    if command.startswith("echo"):
        sys.stdout.write(command[5:])
        

    
if __name__ == "__main__":
    main()
