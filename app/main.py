import sys


def main():
    sys.stdout.write("$ ")
    command = input() 
        
    if command == "exit 0":
        sys.exit(0)
        
    elif command.startswith("echo"):
        sys.stdout.write(command[5:]) 
        
        
    else:
        sys.stdout.write(f"{command} : command not found")
        
    

    
if __name__ == "__main__":
    main()
