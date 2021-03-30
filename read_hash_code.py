class Env:
    def __init__(self):
        self.D = 0
        self.I = 0
        self.S = 0
        self.V = 0
        self.F = 0
    
    def saveInitValues(self, d, i, s, v, f):
        self.D = d
        self.I = i
        self.S = s
        self.V = v
        self.F = f

    def readFile(self, path):
        hashcodeFile = open(path, 'r')
        count = 0
        while True:
            count += 1
        
            # Get next line from file
            line = hashcodeFile.readline()
                
            # if line is empty
            # end of file is reached
            if not line:
                break
            
            if (int(self.S) + 1 >= count > 1):
                print("Line{}: {}".format(count, line.strip()))

            # Read first line and store environment variables
            if (count == 1):
                [d, i, s, v, f] = line.split()
                self.saveInitValues(d, i, s, v, f)

        hashcodeFile.close()

def main():
    env = Env()
    env.readFile('hashcode.in')
    print(f"D={env.D} I={env.I} S={env.S} V={env.V} F={env.F}")
    

if __name__ == "__main__":
    # execute only if run as a script
    main()