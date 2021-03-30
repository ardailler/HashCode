class Vehicle:
    def __init__(self, nb_streets, streets):
        self.NB_Streets = nb_streets # Number of street before destination
        self.Streets = streets # List of streets names (path before destionation)
    
    def print(self):
        print(f"NB_Streets={self.NB_Streets} Streets=[{', '.join(self.Streets)}]")


class Street:
    def __init__(self, id_b, id_e, name, time):
        self.ID_B = id_b # Intersection link to the begging of the street
        self.ID_E = id_e # Intersection link to the endding of the street
        self.Name = name # Name of the street
        self.T = time # Time to travel across the street
    
    def print(self):
        print(f"ID_B={self.ID_B} ID_E={self.ID_E} Name={self.Name} T={self.T}")

'''
to display node graph
? https://www.python-course.eu/networkx.php
'''
class Env:
    def __init__(self):
        self.D = 0 # Duration of the full cycle
        self.I = 0 # Number of intersections
        self.S = 0 # Number of streets
        self.V = 0 # Number of vehicles
        self.F = 0 # Score for each vehicles (when endding their path)
        
    def saveInitValues(self, d, i, s, v, f):
        self.D = d
        self.I = i
        self.S = s
        self.V = v
        self.F = f

    def readFile(self, path):
        hashcodeFile = open(path, 'r')
        count = 0
        intersections_dict = {} # Dictionnary of street grouped by their endding intersections

        while True:
            count += 1
        
            # Get next line from file
            line = hashcodeFile.readline()
                
            # if line is empty
            # end of file is reached
            if not line:
                break

            if (count > 1):
                # Iterate on each street lines
                if (self.S + 1 >= count):
                    [id_b, end_e, name, time] = line.split() # read street line
                    street = Street(id_b, end_e, name, time) # create new Street Object # TODO need to be store
                    intersections_dict.setdefault(end_e,[]).append(street) # append street in it's endding intersection
                    # street.print() # debug to print street infos
                elif (self.S + 1 + self.V >= count):
                    vehicle_infos = line.split() # read street line
                    vehicle = Vehicle(vehicle_infos[0], vehicle_infos[1:]) # TODO need to be store
                    # vehicle.print()
                    # print("Line_{}: {}".format(count, line.strip()))

            # Read first line and store environment variables
            if (count == 1):
                [d, i, s, v, f] = line.split()
                self.saveInitValues(int(d), int(i), int(s), int(v), int(f))
        # print(intersections_dict)
        hashcodeFile.close()

def main():
    env = Env()
    env.readFile('hashcode.in')
    print(f"D={env.D} I={env.I} S={env.S} V={env.V} F={env.F}")
    

if __name__ == "__main__":
    # execute only if run as a script
    main()