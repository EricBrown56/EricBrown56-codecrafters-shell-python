import sys


def main():
    
    command = input() 
        
    if command == "exit 0":
        sys.exit(0)
        
    elif command.startswith("echo"):
        sys.stdout.write(command[5:])
        sys.stdout.write("\n$ ")
        
    else:
        sys.stdout.write(f"{command} : command not found")
        
    

    
if __name__ == "__main__":
    main()
