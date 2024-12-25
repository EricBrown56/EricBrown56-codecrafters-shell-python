import sys


def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        command = input() 
            
        if command == "exit 0":
            sys.exit(0)
            
        elif command.startswith("echo"):
            sys.stdout.write(command[5:] + "\n") 
            
            
        else:
            sys.stdout.write(f"{command}: command not found\n")
            
        

    
if __name__ == "__main__":
    main()
