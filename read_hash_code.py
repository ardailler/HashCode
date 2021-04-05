'''
Vehicle
@param nb_streets (int) : number of streets the car must cross to complete its path
@param streets (string[]) : the list of the street names
@param index (int) : the current position of the car in this list
@param score (int) : the current score of the car 
'''
class Vehicle:
    def __init__(self, nb_streets, streets):
        self.nb_streets = int(nb_streets) # Number of street before destination
        self.streets = streets # List of streets names (path before destionation)
        self.index = 0 # Position in the streets path
        self.score = 0 # the score of the vehicle

    def __repr__(self):
        return str(f"nb_streets={self.nb_streets} streets=[{', '.join(self.streets)}]")

    def print(self):
        print(f"nb_streets={self.nb_streets} streets=[{', '.join(self.streets)}]")

    def getStreet(self):
        return self.streets[self.index]

'''
Street
@param name (string) : The unique name of the street
@param id_b (int) : Intersection link to the begging of the street
@param id_e (int) : Intersection link to the endding of the street
@param T (int) : Time to travel across the street
@param vehicles ((Vehicle, int)[]) : tuple list of vehicle and the time when they arrive at the end of street (ex: if D = 4 and T = 3 => 4 + 3 = 7 : when D >= 7 try to move)
'''
class Street:
    def __init__(self, id_b, id_e, name, time):
        self.name = name # Name of the street
        self.id_b = int(id_b) # Intersection link to the begging of the street
        self.id_e = int(id_e) # Intersection link to the endding of the street
        self.T = int(time) # Time to travel across the street
        self.vehicles = [] # tuple list of vehicle and the time when they arrive at the end of street (vehicle, 2)
    
    def addVehicle(self, vehicle, d):
        if d == 0:
            self.vehicles.append((vehicle, 0))
        else:
            self.vehicles.append((vehicle, (d + self.T)))

    def __repr__(self):
        vehicles = str(f"({v},{i})" for (v, i) in self.vehicles)
        return str(f"id_b={self.id_b} id_e={self.id_e} name={self.name} T={self.T} vehicles={self.vehicles}")

    def print(self):
        vehicles = str(f"({v},{i})" for (v, i) in self.vehicles)
        print(f"id_b={self.id_b} id_e={self.id_e} name={self.name} T={self.T} vehicles={vehicles}")

'''
Intersection
@param id (int) : unique id of the intersection
@param streets_i (Street[]) : List of incomming streets
@param streets_o (Street[]) : List of outgoing streets
@param schedulers ((Street, int)[]) List of tuple (incomming street, duration of green light)
@param index (int) : index of scheduler
'''
class Intersection:
    def __init__(self, id_i):
        self.id = int(id_i)
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

Env
@param D (int) : Duration of the full cycle
@param I (int) : Number of intersections
@param S (int) : Number of streets
@param V (int) : Number of vehicles
@param F (int) : Score for each vehicles (when endding their path)
'''
class Env:
    def __init__(self):
        self.D = 0 # Duration of the full cycle
        self.I = 0 # Number of intersections
        self.S = 0 # Number of streets
        self.V = 0 # Number of vehicles
        self.F = 0 # Score for each vehicles (when endding their path)

        self.streets = {}
        self.intersections = {}
        self.vehicles = []

        self.visited_streets = []
        
    def saveInitValues(self, d, i, s, v, f):
        self.D = int(d)
        self.I = int(i)
        self.S = int(s)
        self.V = int(v)
        self.F = int(f)

    def addOrCreateIntersection(self, id_i, street, inOrOut):
        if id_i in self.intersections: # the case where the intersection already exist
            intersection = self.intersections[id_i]
        else: # Case where the intersection not exist
            intersection = Intersection(id_i)
        
        # selecting the list where we need to add the current street (incomming or outgoing street list)
        if inOrOut == 'in':
            intersection.addStreetI(street)
        elif inOrOut == 'out':
            intersection.addStreetO(street)
        # updating or inserting the intersection
        self.intersections[id_i] = intersection

    def init(self, path):
        self.readFile(path)
        for vehicle in self.vehicles:
            current_street = vehicle.getStreet() # getting the current street of the current vehicle
            self.streets[current_street].addVehicle(vehicle, 0) # adding this vehicle to his street (0 because it's init phase)
            print("-------------------")
            print(current_street)
            print(self.streets[current_street])
        print(self.intersections)


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
                    self.streets[name] = street # adding our street in the env streets dictonnary

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

    def run(self):
        for i in range(self.D): # ? D or (D - 1)
            print(i)


def main():
    env = Env()
    # env.readFile('hashcode.in')
    # print(env.intersections)
    env.init('hashcode.in')
    print(f"D={env.D} I={env.I} S={env.S} V={env.V} F={env.F}")
    

if __name__ == "__main__":
    # execute only if run as a script
    main()