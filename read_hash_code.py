'''
Vehicle
@param nb_streets (int) : number of streets the car must cross to complete its path
@param streets (string[]) : the list of the street names
@param index (int) : the current position of the car in this list
@param score (int) : the current score of the car
@param F (int) : Score for each vehicles (when endding their path)
@param D (int) : Duration of the full cycle
'''
class Vehicle:
    def __init__(self, nb_streets, streets, f, d):
        self.nb_streets = int(nb_streets) # Number of street before destination
        self.streets = streets # List of streets names (path before destionation)
        self.index = 0 # Position in the streets path
        self.score = 0 # the score of the vehicle
        self.F = int(f) # Score for each vehicles (when endding their path)
        self.D = int(d) # Duration of the full cycle

    def isLastStreet(self):
        return self.index == (self.nb_streets - 1)
    
    def calculateScore(self, t):
        self.score = self.F + (self.D - t)

    def getStreet(self):
        return self.streets[self.index]
    
    def step(self):
        self.index += 1

    def __repr__(self):
        return str(f"nb_streets={self.nb_streets} streets=[{', '.join(self.streets)}]")

    def print(self):
        print(f"nb_streets={self.nb_streets} streets=[{', '.join(self.streets)}]")

'''
Street
@param name (string) : The unique name of the street
@param id_b (int) : Intersection link to the begging of the street
@param id_e (int) : Intersection link to the endding of the street
@param L (int) : Time to travel across the street
@param vehicles ((Vehicle, int)[]) : tuple list of vehicle and the time when they arrive at the end of street (ex: if T = 1 and L = 3 => 1 + 3 = 4 : when T = 4 the car is at the end)
'''
class Street:
    def __init__(self, id_b, id_e, name, time):
        self.name = name # Name of the street
        self.id_b = int(id_b) # Intersection link to the begging of the street
        self.id_e = int(id_e) # Intersection link to the endding of the street
        self.L = int(time) # Time to travel across the street
        self.vehicles = [] # tuple list of vehicle and the time when they arrive at the end of street (vehicle, 2)
    
    def addVehicle(self, vehicle, t):
        self.vehicles.append((vehicle, (t + self.L)))
    
    def addInitVehicle(self, vehicle):
        self.vehicles.append((vehicle, 0))

    '''
    deleteVehiclesArrived
    t is the current time already use in this experience
    '''
    def deleteVehiclesArrived(self, t):
        # we iterate the vehicles list in order to check every vehicles inside the current street
        # note : vehicles are iterate on the same order then they was enter in the list (because of append at end of list and iterate from begging)
        for index, (vehicle, time) in enumerate(self.vehicles):
            # checking if the current vehicle is on it's last street and then if he arrived at the end of his last street
            if vehicle.isLastStreet() and time <= t:
                # if it's the case we calculate his score
                vehicle.calculateScore(t)
                # and remove it from the street
                del self.vehicles[index]
    
    def step(self, t):
        if len(self.vehicles) > 0:
            (vehicle, timeWhenMove) = self.vehicles[0]
            if t >= timeWhenMove:
                vehicle.step()
                del self.vehicles[0]
                return vehicle
        return None

    def __repr__(self):
        return str(f"id_b={self.id_b} id_e={self.id_e} name={self.name} L={self.L} vehicles={self.vehicles}")

    def print(self):
        print(f"id_b={self.id_b} id_e={self.id_e} name={self.name} L={self.L} vehicles={self.vehicles}")

'''
Intersection
@param id (int) : unique id of the intersection
@param streets_i (Street[]) : List of incomming streets
@param streets_o (Street[]) : List of outgoing streets
@param schedulers ((Street, int)[]) List of tuple (incomming street, duration of green light)
@param index (int) : index of scheduler@param D (int) : Duration of the full cycle
'''
class Intersection:
    def __init__(self, id_i, d):
        self.id = int(id_i)
        self.streets_i = [] # List of incomming streets
        self.streets_o = [] # List of outgoing streets
        self.schedulers = [] # List of tuple (incomming street, duration of green light)
        self.index = 0 # index of scheduler
        self.D = int(d) # Duration of the full cycle
    
    def addStreetI(self, street):
        self.streets_i.append(street)

    def addStreetO(self, street):
        self.streets_o.append(street)
    
    def addScheduler(self, street, duration, green_since = 0):
        self.schedulers.append((street, duration, green_since))
    
    '''
    Switch to the next green light
    '''
    def nextScheduler(self, t):
        self.index = (self.index + 1) % len(self.schedulers) # go to next traffic light scheduler
        (street, timer, green_since) = self.schedulers[self.index] # isolate values of next green light
        self.schedulers[self.index] = (street, timer, t) # initialise the green light since value

    def step(self, t):
        if (len(self.schedulers) > 0):
            (street, timer, green_since) = self.schedulers[self.index]
            # first we check if we need to switch green light
            if (int(green_since) + int(timer)) == int(t):
                self.nextScheduler(t)
                (street, timer, green_since) = self.schedulers[self.index]
            vehicleToMove = street.step(t)
            if vehicleToMove != None:
                street = vehicleToMove.getStreet()
                index = next((i for i, s in enumerate(self.streets_o) if s.name == street))
                self.streets_o[index].addVehicle(vehicleToMove, t)
            

    def __repr__(self):
        return str(f"\nID={self.id} \n\t streets_i={self.streets_i} \n\t streets_o={self.streets_o} \n\n\t streets_o={self.schedulers}\n\n----------\n")

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
            intersection = Intersection(id_i, self.D)
        
        # selecting the list where we need to add the current street (incomming or outgoing street list)
        if inOrOut == 'in':
            intersection.addStreetI(street)
        elif inOrOut == 'out':
            intersection.addStreetO(street)
        # updating or inserting the intersection
        self.intersections[id_i] = intersection

    '''
    init function
    read the hashcodeFile and
    position all vehicle at the end of their first street
    '''
    def init(self, path):
        self.readFile(path)
        for vehicle in self.vehicles:
            current_street = vehicle.getStreet() # getting the current street of the current vehicle
            self.streets[current_street].addInitVehicle(vehicle) # adding this vehicle to his street (0 because it's init phase)

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

                    self.addOrCreateIntersection(int(id_b), street, 'out') # register this street in the outgoing street list of the intersection id_b
                    self.addOrCreateIntersection(int(id_e), street, 'in') # register this street in the incomming street list of the intersection id_e

                elif (self.S + 1 + self.V >= count):
                    vehicle_infos = line.split() # read street line
                    vehicle = Vehicle(vehicle_infos[0], vehicle_infos[1:], self.F, self.D) # create a new Vehicle
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
        for t in range(self.D): # ? D or (D - 1)
            print(f"{t} / {self.D}", end='\r')
            # before the intersections step we check if their are vehicle that has finish there path
            for id_street, street in self.streets.items():
                street.deleteVehiclesArrived(t)

            for id_inter, intersection in self.intersections.items():
                intersection.step(t)
        
        # ? not sure if we need to do that to
        for id_street, street in self.streets.items():
            street.deleteVehiclesArrived(t)

        return sum(vehicule.score for vehicule in self.vehicles)
    
    def readSubmission(self, path):
        submissionFile = open(path, 'r')
        count = 0

        # Get number of intersections
        nb_iter = int(submissionFile.readline())
        for inter in range(nb_iter):
            id_inter = int(submissionFile.readline())
            nb_green_lights = int(submissionFile.readline())
            for g_light in range(nb_green_lights):
                [street_name, duration] = submissionFile.readline().split()
                self.intersections[id_inter].addScheduler(self.streets[street_name], duration)

        submissionFile.close()

def main():
    env = Env()
    # env.readFile('hashcode.in')
    # print(env.intersections)
    env.init('exemple.in')
    print(f"D={env.D} I={env.I} S={env.S} V={env.V} F={env.F}")
    
    env.readSubmission('exemple_submission.in')
    # print(env.intersections)

    print(f"reward = {env.run()}")

if __name__ == "__main__":
    # execute only if run as a script
    main()

'''
intersection.step()
 -> get scheduler()
    -> if scheduler.duration >= T
        -> then switch light
    -> street.step()
        -> each vehicle
            -> if d >= timeToMove
                -> then vehicle.step()
                -> del vehicle
                -> return vehicle
            -> else return None
        -> if not None
            -> then vehicle.getStreet()
            -> search next in street_o and add vehicle
'''