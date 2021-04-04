class Vehicle:
    def __init__(self, nb_streets, streets):
        self.nb_streets = nb_streets # Number of street before destination
        self.streets = streets # List of streets names (path before destionation)
        self.index = 0 # Position in the streets path
        self.score = 0 # the score of the vehicle

    def __repr__(self):
        return str(f"nb_streets={self.nb_streets} streets=[{', '.join(self.streets)}]")

    def print(self):
        print(f"nb_streets={self.nb_streets} streets=[{', '.join(self.streets)}]")


class Street:
    def __init__(self, id_b, id_e, name, time):
        self.name = name # Name of the street
        self.id_b = id_b # Intersection link to the begging of the street
        self.id_e = id_e # Intersection link to the endding of the street
        self.T = time # Time to travel across the street
        self.vehicles = [] # tuple list of vehicle and the time when they arrive at the end of street (vehicle, 2)

    def __repr__(self):
        return str(f"id_b={self.id_b} id_e={self.id_e} name={self.name} T={self.T}")

    def print(self):
        print(f"id_b={self.id_b} id_e={self.id_e} name={self.name} T={self.T}")
    
class Intersection:
    def __init__(self, id_i):
        self.id = id_i
        self.streets_i = [] # List of incomming streets
        self.streets_o = [] # List of outgoing streets
        self.schedulers = [] # List of tuple (incomming street, duration of green light)
        self.index = 0 # index of scheduler
    
    def addStreetI(self, street):
        self.streets_i.append(street)

    def addStreetO(self, street):
        self.streets_o.append(street)

    def __repr__(self):
        return str(f"\nID={self.id} \n\t streets_i={self.streets_i} \n\t streets_o={self.streets_o}\n\n----------\n")

    def print(self):
        print(f"\nID={self.id} \n\t streets_i={self.streets_i} \n\t streets_o={self.streets_o}\n\n----------\n")

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

        self.streets = []
        self.intersections = {}
        self.vehicles = []

        self.visited_streets = []
        
    def saveInitValues(self, d, i, s, v, f):
        self.D = d
        self.I = i
        self.S = s
        self.V = v
        self.F = f

    def addOrCreateIntersection(self, id_i, street, inOrOut):
        if id_i in self.intersections: # the case where the intersection already exist
            intersection = self.intersections[id_i]
        else: # Case where the intersection not exist
            intersection = Intersection(id_i)
        
        if inOrOut == 'in':
            intersection.addStreetI(street)
        elif inOrOut == 'out':
            intersection.addStreetO(street)
        # updating or inserting the intersection
        self.intersections[id_i] = intersection

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
                    [id_b, id_e, name, time] = line.split() # read street line
                    street = Street(id_b, id_e, name, time) # create new Street Object
                    self.streets.append(street) # adding our street in the env list

                    self.addOrCreateIntersection(id_b, street, 'out') # register this street in the outgoing street list of the intersection id_b
                    self.addOrCreateIntersection(id_e, street, 'in') # register this street in the incomming street list of the intersection id_e

                elif (self.S + 1 + self.V >= count):
                    vehicle_infos = line.split() # read street line
                    vehicle = Vehicle(vehicle_infos[0], vehicle_infos[1:]) # create a new Vehicle
                    self.vehicles.append(vehicle)
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
    print(env.intersections)
    

if __name__ == "__main__":
    # execute only if run as a script
    main()