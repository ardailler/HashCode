def main():
    hashcodeFile = open('hashcode.in', 'r')
    count = 0

    while True:
        count += 1
    
        # Get next line from file
        line = hashcodeFile.readline()
    
        # if line is empty
        # end of file is reached
        if not line:
            break
        print("Line{}: {}".format(count, line.strip()))
    
    hashcodeFile.close()

if __name__ == "__main__":
    # execute only if run as a script
    main()