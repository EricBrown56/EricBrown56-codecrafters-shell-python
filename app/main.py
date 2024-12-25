import sys


def main():
    sys.stdout.write("$ ")
    while True:
        command = input()
        if command == "exit":
            break
        print(f"{command}: command not found")
        sys.stdout.write("$ ")
    

    
if __name__ == "__main__":
    main()
