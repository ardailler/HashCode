class Vehicle:
    def __init__(self, nb_streets, streets):
        self.nb_streets = nb_streets # Number of street before destination
        self.streets = streets # List of streets names (path before destionation)
        self.index = 0 # Position in the streets path
        self.score = 0 # the score of the vehicle

    def print(self):
        print(f"nb_streets={self.nb_streets} streets=[{', '.join(self.streets)}]")


class Street:
    def __init__(self, id_b, id_e, name, time):
        self.name = name # Name of the street
        self.id_b = id_b # Intersection link to the begging of the street
        self.id_e = id_e # Intersection link to the endding of the street
        self.T = time # Time to travel across the street
        self.vehicles = [] # tuple list of vehicle and the time when they arrive at the end of street (vehicle, 2)

    def print(self):
        print(f"id_b={self.id_b} id_e={self.id_e} name={self.name} T={self.T}")
    
class Intersection:
    def ___init___(self, id, streets_i, streets_o, schedulers):
        self.id = id
        self.streets_i = streets_i # List of incomming streets
        self.streets_o = streets_o # List of outgoing streets
        self.schedulers = schedulers # List of tuple (incomming street, duration of green light)
        self.index = 0 # index of scheduler

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
        self.intersections = []
        self.vehicles = []

        self.visited_streets = []
        
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
                    street = Street(id_b, end_e, name, time) # create new Street Object
                    self.streets.append(street)
                    # intersections_dict.setdefault(end_e,[]).append(street) # append street in it's endding intersection
                    # print(end_e)
                    # self.intersections[end_e] += [street] # append street in it's endding intersection TODO self.addIntersection (id, street, 'in/out')
                    # street.print() # debug to print street infos
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
    

if __name__ == "__main__":
    # execute only if run as a script
    main()