import sys


def main():
    sys.stdout.write("$ ")
    while True:
        command = input()
        if command == "exit 0":
            break
        
        sys.stdout.write("$ ")
    if command == "echo <text>":
        sys.stdout.write("<text>\n")
        

    
if __name__ == "__main__":
    main()
