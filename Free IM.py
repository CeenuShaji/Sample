#Free IM

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import time
import heapq
from prettytable import PrettyTable
import copy
import threading
import csv
from queue import Queue
import datetime

current_node='not_updating'

class Vehicle:
    def __init__(self, ID, origin, destination, time_to_reach_intersection, time_to_cross, current_node):
        self.ID = ID

        if origin.lower() in ['east', 'west', 'north', 'south']:
            self.origin = origin
        elif destination.lower() in ['east', 'west', 'north', 'south']:
            self.destination = destination
        else:
            raise ValueError("Invalid origin.")

        self.destination = destination
        self.time_to_reach_intersection = float(time_to_reach_intersection)
        self.time_to_cross = time_to_cross
        self.current_node = current_node

# Four arrays of request signal, each for each direction
north_queue = []
south_queue = []
east_queue = []
west_queue = []


# Queues the REQUEST signal and assumes they all get CONFIRM signal from Int. BEFORE MOVING
NO=[]
NL=[]
NR=[]
NS=[]

SR=[]
SL=[]
SO=[]
SS=[]

EO=[]
EL=[]
ER=[]
ES=[]

WR=[]
WL=[]
WO=[]
WS=[]


class Node:
    def __init__(self):
        self.vehicles = []
        self.time = 0
        self.presence = False

Node1 = Node()
Node2 = Node()
Node3 = Node()
Node4 = Node()
Node5 = Node()
Node6 = Node()
Node7 = Node()
Node8 = Node()
Node9 = Node()
Node10 = Node()
Node11 = Node()
Node12 = Node()
Node13 = Node()
Node14 = Node()
Node15 = Node()
Node16 = Node()

Exited_north = Node()
Exited_south = Node()
Exited_east = Node()
Exited_west = Node()

all_queues = [SO, SR, SL, NO, NR, NL, EO, ER, EL, WO, WR, WL, SS, NS, WS, ES]  
save_all_queues = {
    'SR': SR, 'SL': SL, 'NO': NO, 'NR': NR, 'NL': NL, 'EO': EO, 'ER': ER, 'EL': EL, 'WO': WO, 'WR': WR, 'WL': WL,
    'SS': SS, 'NS': NS, 'ES': ES, 'WS': WS
}
queue_order_NSEW=[]
FROsorted_queue=[]
node_headway_seconds=2

moved_vehicles=[]

# Initialize current_node to None
#current_node = None 

# Initialize vehicle IDs and the queue
vehicle_ids = set("emergency" + str(i) for i in range(20)) | set(str(i) for i in range(40))
def print_queue(queue):
    if not queue:  # Check if the queue is empty
        print("\nEmpty Queue!!")
    else:
        count = 0
        print("\n")
        for vehicle in queue:
            count += 1
            print("Vehicle #", count, ".", vehicle.ID)

def print_vehicles(queue, queue_name):
    #print(queue, queue_name)

    table = PrettyTable()
    table.field_names = ["Index", "Vehicle ID", "Time to Reach", "Origin", "Current Node", "Destination"]
    for count, vehicle in enumerate(queue, 1): #initialize count to one
        
        table.add_row([count, vehicle.ID, vehicle.time_to_reach_intersection, vehicle.origin, vehicle.current_node, vehicle.destination])
        

    print(f"\n{queue_name} Queue:")
    print(table)

# Function to get the name of the queue from its value
def get_queue_name(queue_value):
    # Create a dictionary to map the queue names to their corresponding values
    queues_dict = {
        'SO': SO,
        'SR': SR,
        'SL': SL,
        'NO': NO,
        'NR': NR,
        'NL': NL,
        'EO': EO,
        'ER': ER,
        'EL': EL,
        'WO': WO,
        'WR': WR,
        'WL': WL,

        'SS': SS,
        'NS': NS,
        'ES': ES,
        'WS': WS,
    }

    for name, value in queues_dict.items():
        if value is queue_value:
            return name
    return None

def get_queue_name_forEV(queue_value):
    # Create a dictionary to map the queue names to their corresponding values
    queues_dict = {
        'SO': SO,
        'SR': SR,
        'SL': SL,
        'NO': NO,
        'NR': NR,
        'NL': NL,
        'EO': EO,
        'ER': ER,
        'EL': EL,
        'WO': WO,
        'WR': WR,
        'WL': WL,

        'SS': SS,
        'NS': NS,
        'ES': ES,
        'WS': WS,
    }

    for name, value in queues_dict.items():
        if value is queue_value:
            
            return name
    
####################  STORAGE ZONE  #####################################    
    
def queue_vehicle_request_from_origin(vehicle, origin):
    if vehicle.origin == 'north':
        north_queue.append(vehicle)
        if vehicle.destination == 'south':
            #if len(SO) < 3: #needs for Networkx
            NO.append(vehicle)
            vehicle.current_node = 'NO'
        
        elif vehicle.destination == 'east':
            #if len(SR) < 3:
            NL.append(vehicle)
            vehicle.current_node = 'NL'

        elif vehicle.destination == 'west':
            #if len(SL) < 3:
            NR.append(vehicle)
            vehicle.current_node = 'NR'
       
    elif vehicle.origin == 'south':
        south_queue.append(vehicle)
        if vehicle.destination == 'north':
            #if len(NO) < 3:
            SO.append(vehicle)
            vehicle.current_node = 'SO'
        
        elif vehicle.destination == 'east':
            #if len(NL) < 3:
            SR.append(vehicle)
            vehicle.current_node = 'SR'

        elif vehicle.destination == 'west':
            #if len(NR) < 3:
            SL.append(vehicle)
            vehicle.current_node = 'SL'
    
    elif vehicle.origin == 'east':
        east_queue.append(vehicle)
        if vehicle.destination == 'north':
            #if len(ER) < 3:
            ER.append(vehicle)
            vehicle.current_node = 'ER'
        
        elif vehicle.destination == 'south':
            #if len(EL) < 3:
            EL.append(vehicle)
            vehicle.current_node = 'EL'

        elif vehicle.destination == 'west':
            #if len(EO) < 3:
            EO.append(vehicle)
            vehicle.current_node = 'EO'
    
    elif vehicle.origin == 'west':
        west_queue.append(vehicle)
        if vehicle.destination == 'north':

            WL.append(vehicle)
            vehicle.current_node = 'WL'
        
        elif vehicle.destination == 'east':
            #print("I am here")
            WO.append(vehicle)
            vehicle.current_node = 'WO'
        

        elif vehicle.destination == 'south':
            #WR.vehicle.current_node = 'WR'
            WR.append(vehicle)
            vehicle.current_node = 'WR'
            
def random_NSEWvehicle_REQUESTS():
    global queue_order_NSEW, current_node
    # Initialize the queue
    queue_order_NSEW = []
    count=1
    print("\nTraffic flow:")
    # Randomly queue the north and south directions with vehicles
    table = PrettyTable()
    table.field_names = ["Index", "Vehicle ID", "Time to Reach", "Origin", "Dest", "Current Node", "Message_byIM"]

    origin_counts = {'east': 0, 'west': 0, 'north': 0, 'south': 0}
    destination_counts = {'south': 0, 'north': 0, 'east': 0, 'west': 0}


    for origin in random.choices(['east', 'west', 'north', 'south'], k=36):

        if origin_counts[origin] >= 9:
            continue
            
        veh_id = random.choice(list(vehicle_ids))
        vehicle_ids.remove(veh_id)  # Remove the used ID from the set
        
        available_destinations = ['east', 'west', 'north', 'south']
        available_destinations.remove(origin)  # Remove the origin from the available destinations
        destination = random.choice(available_destinations)

        time_tocross = 20
        
        # Randomly assign distinct times to each vehicle in the destination lane
        time_to_reach_list = random.sample([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 10)

         # Use the origin_counts to access the correct time from the time_to_reach_list
        time_to_reach_intersection = time_to_reach_list[destination_counts[destination] % 10]

        #current_node='abc'

        vehicle_instance = Vehicle(veh_id, origin, destination, time_to_reach_intersection, time_tocross, current_node)
        
        queue_vehicle_request_from_origin(vehicle_instance, origin)
     
        origin_counts[origin] += 1
        
       
        queue_order_NSEW.append(vehicle_instance)

        message_byIM = "REQUEST"
        table.add_row([count, vehicle_instance.ID, time_to_reach_intersection, vehicle_instance.origin, vehicle_instance.destination, vehicle_instance.current_node, message_byIM])
        count+=1

        destination_counts[destination] += 1  # Update destination_counts
        #Check if the destination queue has less than 3 vehicles before populating
        if (vehicle_instance.destination == 'south' and len(SO) >= 3) or \
           (vehicle_instance.destination == 'north' and len(NO) >= 3) or \
           (vehicle_instance.destination == 'east' and len(EO) >= 3) or \
           (vehicle_instance.destination == 'west' and len(WO) >= 3) or \
           (vehicle_instance.destination == 'south' and len(SR) >= 3) or \
           (vehicle_instance.destination == 'north' and len(NR) >= 3) or \
           (vehicle_instance.destination == 'east' and len(ER) >= 3) or \
           (vehicle_instance.destination == 'west' and len(WR) >= 3) or \
           (vehicle_instance.destination == 'south' and len(SL) >= 3) or \
           (vehicle_instance.destination == 'north' and len(NL) >= 3) or \
           (vehicle_instance.destination == 'east' and len(EL) >= 3) or \
           (vehicle_instance.destination == 'west' and len(WL) >= 3):
            continue
    #print_queue(queue_order_NSEW)
    print(table)



def arrange_vehicle_requests_by_time(queue_order):
    # Sort the vehicles in descending order based on time to reach 
    # First Ready Out
    global FROsorted_queue
    FROsorted_queue = sorted(queue_order, key=lambda vehicle: vehicle.time_to_reach_intersection)

    # Create a table
    table = PrettyTable()
    table.field_names = ["Index", "Vehicle ID", "Time to Reach", "Origin", "Current Node", "message_byIM"]

    # Print the new order of vehicles and add rows to the table
    print("\nNew order of vehicles (First one Ready goes First):")
    for index, vehicle in enumerate(FROsorted_queue):
        message_byIM = "CONFIRM"
        table.add_row([index + 1, vehicle.ID, vehicle.time_to_reach_intersection, vehicle.origin, vehicle.current_node, message_byIM])
  
    # Sort the destination queues based on time_to_reach_intersection for destination queues
    destination_queues = [NO, NL, NR, SO, SR, SL, EO, EL, ER, WO, WR, WL]

    for queue in destination_queues:
        queue.sort(key=lambda vehicle: vehicle.time_to_reach_intersection)

    # Print the table
    print(table)

    return FROsorted_queue

#random_NSEWvehicle_REQUESTS() #None after len>3.. change that
# print_vehicles(WO, 'WO')
# print_vehicles(WR, 'WR')
# print_vehicles(WL, 'WL')

# print_vehicles(EO, 'EO')
# print_vehicles(ER, 'ER')
# print_vehicles(EL, 'EL')

#current_node not available outside randomn and arrange
#arrange_vehicle_requests_by_time(queue_order_NSEW)



def rtrnListName(array_name):
    for i in array_name:

        print("@@@@@@@@@@@@@@@@", i.ID)
    # Using globals() to get the variables defined in the global scope
    for name, value in globals().items():
        if value is array_name:
            return name


# Update the global variable all_queues as well
#all_queues = [SO, SR, SL, NO, NR, NL, EO, ER, EL, WO, WR, WL, SS, NS, WS, ES]

#2 Trial
def handle_emergency_vehicle(incoming):
    # Create a dictionary to map the second letter of array to the adjacent queue identifier
    adjacent_yielding_queue_map = {
        'L': 'O',  # For 'LEFT', adjacent queue is 'OPPOSITE' (e.g., SL -> SO)
        'O': 'R',  # For 'OPPOSITE', adjacent queue is 'RIGHT' (e.g., SO -> SR)
        'R': 'S',  # For 'RIGHT', adjacent queue is 'SHOULDER' (e.g., ER -> ES)
    }

    # Create a reverse mapping for the adjacent queue identifier back to the original queue identifier
    adjacent_yielding_queue_map_reverse = {
        'O': 'L',
        'R': 'O',
        'S': 'R',
       
    }
    for vehicle in incoming:
        if vehicle.ID.startswith('emergency'):
            emergency_vehicle = vehicle
            break
    else:
        return  # No emergency vehicle found in incoming queue

    # Move vehicles before the emergency vehicle to an adjacent queue
    emergency_vehicle_index = incoming.index(emergency_vehicle)
    # New queue of vehicles before the index of the emergency vehicle, [::-1] makes sure of reversing it ensuring that the vehicles are moved in the order they were originally queued.
    vehicles_to_move = incoming[:emergency_vehicle_index][::-1]  # Reverse to maintain the order
  
    

    origin_queue_name = get_queue_name(incoming)  # Get the original queue name from the incoming input
    #print("################", origin_queue_name)
    adjacent_queue_id = origin_queue_name[0] + adjacent_yielding_queue_map[origin_queue_name[1]]
    adjacent_queue = next(q for q in all_queues if get_queue_name(q) == adjacent_queue_id)
    #print("############", adjacent_queue)
    veh_togoback = adjacent_queue[:emergency_vehicle_index]

    # Move vehicles before the emergency vehicle to an adjacent queue
    #while incoming[0] != emergency_vehicle:
    for vehicle in vehicles_to_move:
        # if emergency_vehicle in vehicles_to_move:
        #     print("##########################Emergency vehicle is in veh_to_goback")
        vehicle = incoming.pop(0)
        adjacent_queue.append(vehicle)
        #print("#############", adjacent_queue)
        print(f"\n\tEV MOVE: Moved Vehicle ID {vehicle.ID} from {origin_queue_name} to {get_queue_name(adjacent_queue)} at ", datetime.datetime.now().strftime("%I:%M:%S %p"))
        #print(f"\nEV MOVE: Moved Vehicle ID {vehicle.ID} from {origin_queue_name} to {get_queue_name(adjacent_queue)}")
        # Check if the emergency vehicle is in the list veh_to_goback

        time.sleep(1)
    # for u in veh_togoback:
    #     print("\n#############",u.ID)
    # Move vehicles back from the adjacent queue to their original queue
    #while len(adjacent_queue) > 0:
    for vehicle in adjacent_queue:
        # if emergency_vehicle in veh_togoback:
        #     print("##########################Emergency vehicle is ")#, veh_togoback[])
        vehicle = adjacent_queue.pop(0)
        #vehicle_back = adjacent_queue.pop(0)
        adjacent_reverse_id = adjacent_queue_id[0] + adjacent_yielding_queue_map_reverse[adjacent_queue_id[1]]
        original_queue = next(q for q in all_queues if get_queue_name(q) == adjacent_reverse_id)
        original_queue.append(vehicle)
        if not vehicle.ID.startswith('emergency'):
            print(f"\nEV MOVE BACK: Moved Vehicle ID {vehicle.ID} from adjacent queue back to {get_queue_name(original_queue)} at ", datetime.datetime.now().strftime("%I:%M:%S %p"))
        else:
            print("\nEMergency vehicle exited")
        time.sleep(1)


#2 Clear the vehicles in front
def remove_veh_in_front(incoming):
    # Create a dictionary to map the second letter of array to the adjacent queue identifier
  #........
    for vehicle in incoming:
        if vehicle.ID.startswith('emergency'):
            emergency_vehicle = vehicle
            break
    else:
        return  # No emergency vehicle found in incoming queue

    # Move vehicles before the emergency vehicle to an adjacent queue
    emergency_vehicle_index = incoming.index(emergency_vehicle)
    # New queue of vehicles before the index of the emergency vehicle, [::-1] makes sure of reversing it ensuring that the vehicles are moved in the order they were originally queued.
    vehicles_to_move = incoming[:emergency_vehicle_index][::-1]  # Reverse to maintain the order
    
    # for i in vehicles_to_move:
    #     print("Vehicle in front of EV", i.ID)
    

    origin_queue_name = get_queue_name(incoming)  # Get the original queue name from the incoming input
    #print("################", origin_queue_name)
    #adjacent_queue_id = origin_queue_name[0] + adjacent_yielding_queue_map[origin_queue_name[1]]
    #adjacent_queue = next(q for q in all_queues if get_queue_name(q) == adjacent_queue_id)
    #print("############", adjacent_queue)
    #veh_togoback = adjacent_queue[:emergency_vehicle_index]

    # Move vehicles before the emergency vehicle to an adjacent queue
    #while incoming[0] != emergency_vehicle:
    for vehicle in vehicles_to_move:
        # if emergency_vehicle in vehicles_to_move:
        #     print("##########################Emergency vehicle is in veh_to_goback")
        vehicle = incoming.pop(0)
        #adjacent_queue.append(vehicle)
        #print("#############", adjacent_queue)
        
        print(f"\n\tYIELDing to {emergency_vehicle.ID}: Vehicle {vehicle.ID} moved from {origin_queue_name} at ", datetime.datetime.now().strftime("%I:%M:%S %p"))
        #print(f"\nEV MOVE: Moved Vehicle ID {vehicle.ID} from {origin_queue_name} to {get_queue_name(adjacent_queue)}")
        # Check if the emergency vehicle is in the list veh_to_goback
        #moved_vehicles.append(vehicle)
        queue_vehicle_request_from_origin(vehicle, vehicle.origin)

        time.sleep(1)
    # for u in veh_togoback:
    #     print("\n#############",u.ID)
    # Move vehicles back from the adjacent queue to their original queue
    #while len(adjacent_queue) > 0:

    # for vehicle in adjacent_queue:
    #     # if emergency_vehicle in veh_togoback:
    #     #     print("##########################Emergency vehicle is ")#, veh_togoback[])
    #     vehicle = adjacent_queue.pop(0)
    #     #vehicle_back = adjacent_queue.pop(0)
    #     adjacent_reverse_id = adjacent_queue_id[0] + adjacent_yielding_queue_map_reverse[adjacent_queue_id[1]]
    #     original_queue = next(q for q in all_queues if get_queue_name(q) == adjacent_reverse_id)
    #     original_queue.append(vehicle)
    #     if not vehicle.ID.startswith('emergency'):
    #         print(f"\nEV MOVE BACK: Moved Vehicle ID {vehicle.ID} from adjacent queue back to {get_queue_name(original_queue)} at ", datetime.datetime.now().strftime("%I:%M:%S %p"))
    #     else:
    #         print("\nEMergency vehicle exited")
    #     time.sleep(1)



# CONFLICT ZONE MOVEMENT
def define_Nodes(incoming):
    global Node1, Node2, Node3, Node4, Node5, Node6, Node7, Node8, Node9, Node10, Node11, Node12, Node13, Node14, Node15, Node16, Exited_north, Exited_south, Exited_east, Exited_west
    count=0
    
    # Check if there's an emergency vehicle
    has_emergency_vehicle = any(vehicle.ID.startswith('emergency') for vehicle in incoming)

    # If there's an emergency vehicle, handle it first
    if has_emergency_vehicle:
        #handle_emergency_vehicle(incoming)
        remove_veh_in_front(incoming)
        #time.sleep(node_headway_seconds)


    for i in range(len(incoming)):
        
        veh = incoming[0]  # starting from the first vehicle and onwards
        # print(i,"\n")
        # print(incoming,"\n")
        # print(veh,"\n")

        if veh.origin == 'south':
            if veh.destination == 'north':
                while not (Node1.presence or Node2.presence or Node3.presence or Node4.presence):
                    if incoming[0].ID == veh.ID:
                        incoming.pop(0)
                        Node1.vehicles.append(veh.ID)
                        Node1.presence = True
                        Node1.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        veh.current_node = 'Node1'
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node1 at time {Node1.time}")
                        
                        time.sleep(node_headway_seconds)

                        Node1.vehicles.pop(0)
                        Node1.presence = False
                        Node1.time = 0
                        Node2.vehicles.append(veh.ID)
                        Node2.presence = True
                        Node2.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node2 at time {Node2.time}")
                        
                        veh.current_node = 'Node2'
                        time.sleep(node_headway_seconds)

                        Node2.vehicles.pop(0)
                        Node2.presence = False
                        Node2.time = 0
                        Node3.vehicles.append(veh.ID)
                        Node3.presence = True
                        Node3.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node3 at time {Node3.time}")
                        veh.current_node = 'Node3'
                        time.sleep(node_headway_seconds)
                        

                        Node3.vehicles.pop(0)
                        Node3.presence = False
                        Node3.time = 0
                        Node4.vehicles.append(veh.ID)
                        Node4.presence = True
                        Node4.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node4 at time {Node4.time}")
                        veh.current_node = 'Node4'
                        time.sleep(node_headway_seconds)
                        

                        Node4.vehicles.pop(0)
                        Node4.presence = False
                        Node4.time = 0
                        Exited_north.vehicles.append(veh.ID)
                        Exited_north.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) exited to north at time {Exited_north.time}")
                        veh.current_node = 'Exited_north'
                        time.sleep(node_headway_seconds)
                        break

            if veh.destination == 'west':
                while not (Node6.presence or Node8.presence or Node11.presence or Node10.presence):
                    if incoming[0].ID == veh.ID:
                        incoming.pop(0)
                        Node6.vehicles.append(veh.ID)
                        Node6.presence = True
                        Node6.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node6 at time {Node6.time}")
                        veh.current_node = 'Node6'
                        time.sleep(node_headway_seconds)

                        Node6.vehicles.pop(0)
                        Node6.presence = False
                        Node6.time = 0
                        Node8.vehicles.append(veh.ID)
                        Node8.presence = True
                        Node8.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node8 at time {Node8.time}")
                        veh.current_node = 'Node8'
                        time.sleep(node_headway_seconds)

                        Node8.vehicles.pop(0)
                        Node8.presence = False
                        Node8.time = 0
                        Node11.vehicles.append(veh.ID)
                        Node11.presence = True
                        Node11.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node11 at time {Node11.time}")
                        veh.current_node = 'Node11'
                        time.sleep(node_headway_seconds)

                        Node11.vehicles.pop(0)
                        Node11.presence = False
                        Node11.time = 0
                        Node10.vehicles.append(veh.ID)
                        Node10.presence = True
                        Node10.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node10 at time {Node10.time}")
                        veh.current_node = 'Node10'
                        time.sleep(node_headway_seconds)

                        Node10.vehicles.pop(0)
                        Node10.presence = False
                        Node10.time = 0
                        Exited_west.vehicles.append(veh.ID)
                        Exited_west.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) exited to west at time {Exited_west.time}")
                        veh.current_node = 'Exited_west'
                        time.sleep(node_headway_seconds)
                        break

            if veh.destination == 'east':
                if incoming[0].ID == veh.ID:
                    incoming.pop(0)
                    Exited_east.vehicles.append(veh.ID)
                    Exited_east.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                    #print(f"For {veh.origin} to {veh.destination}\n")
                    print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) exited to (righ turn) east at time {Exited_east.time}")
                    veh.current_node = 'Right_Exited_east'
                    time.sleep(node_headway_seconds)
                    break

        if veh.origin == 'north':
            print(veh.ID)
            if veh.destination == 'east':
                while not (Node16.presence or Node15.presence or Node3.presence or Node5.presence):
                    # if not incoming:
                    #     break
                    print(count)
                    if incoming[0].ID == veh.ID:
                        print(veh.ID, " in east")
                        incoming.pop(0)
                        Node16.vehicles.append(veh)
                        Node16.presence = True
                        Node16.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node16 at time {Node16.time}")
                        veh.current_node = 'Node16'
                        time.sleep(node_headway_seconds)

                        Node16.vehicles.pop(0)
                        Node16.presence = False
                        Node16.time = 0
                        Node15.vehicles.append(veh)
                        Node15.presence = True
                        Node15.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node15 at time {Node15.time}")
                        veh.current_node = 'Node15'
                        time.sleep(node_headway_seconds)

                        Node15.vehicles.pop(0)
                        Node15.presence = False
                        Node15.time = 0
                        Node3.vehicles.append(veh)
                        Node3.presence = True
                        Node3.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node3 at time {Node3.time}")
                        veh.current_node = 'Node3'
                        time.sleep(node_headway_seconds)

                        Node3.vehicles.pop(0)
                        Node3.presence = False
                        Node3.time = 0
                        Node5.vehicles.append(veh)
                        Node5.presence = True
                        Node5.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node5 at time {Node5.time}")
                        veh.current_node = 'Node5'
                        time.sleep(node_headway_seconds)

                        Node5.vehicles.pop(0)
                        Node5.presence = False
                        Node5.time = 0
                        Exited_east.vehicles.append(veh)
                        Exited_east.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) exited to east at time {Exited_east.time}")
                        veh.current_node = 'Existed East'
                        time.sleep(node_headway_seconds)
                        break
                        #Node16.presence, Node15.presence, Node3.presence, Node5.presence = False, False, False, False
                        # count+=1
                        # if count==len(incoming):
                        #     break
                        #i+=1
            if veh.destination == 'south':
                while not (Node13.presence or Node12.presence or Node11.presence or Node9.presence):
                    # if not incoming:
                    #     break
                    

                    if incoming[0].ID == veh.ID:
                        incoming.pop(0)
                        Node13.vehicles.append(veh)
                        Node13.presence = True
                        Node13.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node13 at time {Node13.time}")
                        veh.current_node = 'Node13'
                        time.sleep(node_headway_seconds)

                        Node13.vehicles.pop(0)
                        Node13.presence = False
                        Node13.time = 0
                        Node12.vehicles.append(veh)
                        Node12.presence = True
                        Node12.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node12 at time {Node12.time}")
                        veh.current_node = 'Node12'
                        time.sleep(node_headway_seconds)

                        Node12.vehicles.pop(0)
                        Node12.presence = False
                        Node12.time = 0
                        Node11.vehicles.append(veh)
                        Node11.presence = True
                        Node11.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node11 at time {Node11.time}")
                        veh.current_node = 'Node11'
                        time.sleep(node_headway_seconds)

                        Node11.vehicles.pop(0)
                        Node11.presence = False
                        Node11.time = 0
                        Node9.vehicles.append(veh)
                        Node9.presence = True
                        Node9.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node9 at time {Node9.time}")
                        veh.current_node = 'Node9'
                        time.sleep(node_headway_seconds)

                        Node9.vehicles.pop(0)
                        Node9.presence = False
                        Node9.time = 0
                        Exited_south.vehicles.append(veh)
                        Exited_south.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) exited to south at time {Exited_south.time}")
                        veh.current_node = 'Exited_south'
                        time.sleep(node_headway_seconds)
                        break
                        # count+=1
                        # if count==len(incoming):
                        #     break
                    
            if veh.destination == 'west':
                # if not incoming:
                #     break
                if incoming[0].ID == veh.ID:
                    incoming.pop(0)
                    Exited_east.vehicles.append(veh)
                    Exited_east.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                    #print(f"For {veh.origin} to {veh.destination}\n")
                    print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) exited to (right turn) east at time {Exited_east.time}")
                    veh.current_node = 'Existed_east'
                    time.sleep(node_headway_seconds)
                    break
                # count+=1
                # if count==len(incoming):
                #     break

        if veh.origin == 'east':
            if veh.destination == 'south':
                while not (Node5.presence or Node2.presence or Node7.presence or Node6.presence):
                    if incoming[0].ID == veh.ID:
                        incoming.pop(0)
                        Node5.vehicles.append(veh.ID)
                        Node5.presence = True
                        Node5.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node5 at time {Node5.time}")
                        veh.current_node = 'Node5'
                        time.sleep(node_headway_seconds)

                        Node5.vehicles.pop(0)
                        Node5.presence = False
                        Node5.time = 0
                        Node2.vehicles.append(veh.ID)
                        Node2.presence = True
                        Node2.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node2 at time {Node2.time}")
                        veh.current_node = 'Node2'
                        time.sleep(node_headway_seconds)

                        Node2.vehicles.pop(0)
                        Node2.presence = False
                        Node2.time = 0
                        Node7.vehicles.append(veh.ID)
                        Node7.presence = True
                        Node7.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node7 at time {Node7.time}")
                        veh.current_node = 'Node7'
                        time.sleep(node_headway_seconds)

                        Node7.vehicles.pop(0)
                        Node7.presence = False
                        Node7.time = 0
                        Node6.vehicles.append(veh.ID)
                        Node6.presence = True
                        Node6.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node6 at time {Node6.time}")
                        veh.current_node = 'Node6'
                        time.sleep(node_headway_seconds)

                        Node6.vehicles.pop(0)
                        Node6.presence = False
                        Node6.time = 0
                        Exited_south.vehicles.append(veh.ID)
                        Exited_south.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) exited to south at time {Exited_south.time}")
                        time.sleep(node_headway_seconds)
                        veh.current_node = 'Exited_south'
                        break

            if veh.destination == 'west':
                while not (Node4.presence or Node15.presence or Node14.presence or Node13.presence):
                    if incoming[0].ID == veh.ID:
                        incoming.pop(0)
                        Node4.vehicles.append(veh.ID)
                        Node4.presence = True
                        Node4.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node4 at time {Node4.time}")
                        veh.current_node = 'Node4'
                        time.sleep(node_headway_seconds)

                        Node4.vehicles.pop(0)
                        Node4.presence = False
                        Node4.time = 0
                        Node15.vehicles.append(veh.ID)
                        Node15.presence = True
                        Node15.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node15 at time {Node15.time}")
                        veh.current_node = 'Node15'
                        time.sleep(node_headway_seconds)

                        Node15.vehicles.pop(0)
                        Node15.presence = False
                        Node15.time = 0
                        Node14.vehicles.append(veh.ID)
                        Node14.presence = True
                        Node14.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node14 at time {Node14.time}")
                        veh.current_node = 'Node14'
                        time.sleep(node_headway_seconds)

                        Node14.vehicles.pop(0)
                        Node14.presence = False
                        Node14.time = 0
                        Node13.vehicles.append(veh.ID)
                        Node13.presence = True
                        Node13.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node13 at time {Node13.time}")
                        veh.current_node = 'Node13'
                        time.sleep(node_headway_seconds)

                        Node13.vehicles.pop(0)
                        Node13.presence = False
                        Node13.time = 0
                        Exited_west.vehicles.append(veh.ID)
                        Exited_west.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) exited to west at time {Exited_west.time}")
                        veh.current_node = 'Exited_west'
                        time.sleep(node_headway_seconds)
                        break

            if veh.destination == 'north':
                if incoming[0].ID == veh.ID:
                    incoming.pop(0)
                    Exited_south.vehicles.append(veh.ID)
                    Exited_south.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                    #print(f"For {veh.origin} to {veh.destination}\n")
                    print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) exited to (right turm) south at time {Exited_south.time}")
                    veh.current_node = 'Right_Exited_South'
                    time.sleep(node_headway_seconds)
                    break

        if veh.origin == 'west':
            if veh.destination == 'east':
                while not (Node10.presence or Node12.presence or Node14.presence or Node16.presence):
                    if incoming[0].ID == veh.ID:
                        incoming.pop(0)
                        Node10.vehicles.append(veh.ID)
                        Node10.presence = True
                        Node10.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node10 at time {Node10.time}")
                        veh.current_node = 'Node10'
                        time.sleep(node_headway_seconds)

                        Node10.vehicles.pop(0)
                        Node10.presence = False
                        Node10.time = 0
                        Node12.vehicles.append(veh.ID)
                        Node12.presence = True
                        Node12.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node12 at time {Node12.time}")
                        veh.current_node = 'Node12'
                        time.sleep(node_headway_seconds)

                        Node12.vehicles.pop(0)
                        Node12.presence = False
                        Node12.time = 0
                        Node14.vehicles.append(veh.ID)
                        Node14.presence = True
                        Node14.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node14 at time {Node14.time}")
                        veh.current_node = 'Node14'
                        time.sleep(node_headway_seconds)

                        Node14.vehicles.pop(0)
                        Node14.presence = False
                        Node14.time = 0
                        Node16.vehicles.append(veh.ID)
                        Node16.presence = True
                        Node16.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node16 at time {Node16.time}")
                        veh.current_node = 'Node16'
                        time.sleep(node_headway_seconds)

                        Node16.vehicles.pop(0)
                        Node16.presence = False
                        Node16.time = 0
                        Exited_north.vehicles.append(veh.ID)
                        Exited_north.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) exited to north at time {Exited_north.time}")
                        veh.current_node = 'Exited_north'
                        time.sleep(node_headway_seconds)
                        break

            if veh.destination == 'east':
                while not (Node9.presence or Node8.presence or Node7.presence or Node1.presence):
                    if incoming[0].ID == veh.ID:
                        incoming.pop(0)
                        Node9.vehicles.append(veh.ID)
                        Node9.presence = True
                        Node9.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node9 at time {Node9.time}")
                        veh.current_node = 'Node9'
                        time.sleep(node_headway_seconds)

                        Node9.vehicles.pop(0)
                        Node9.presence = False
                        Node9.time = 0
                        Node8.vehicles.append(veh.ID)
                        Node8.presence = True
                        Node8.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node8 at time {Node8.time}")
                        veh.current_node = 'Node8'
                        time.sleep(node_headway_seconds)

                        Node8.vehicles.pop(0)
                        Node8.presence = False
                        Node8.time = 0
                        Node7.vehicles.append(veh.ID)
                        Node7.presence = True
                        Node7.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node7 at time {Node7.time}")
                        veh.current_node = 'Node7'
                        time.sleep(node_headway_seconds)

                        Node7.vehicles.pop(0)
                        Node7.presence = False
                        Node7.time = 0
                        Node1.vehicles.append(veh.ID)
                        Node1.presence = True
                        Node1.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node1 at time {Node1.time}")
                        veh.current_node = 'Node1'
                        time.sleep(node_headway_seconds)

                        Node1.vehicles.pop(0)
                        Node1.presence = False
                        Node1.time = 0
                        Exited_east.vehicles.append(veh.ID)
                        Exited_east.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) exited to east at time {Exited_east.time}")
                        veh.current_node = 'Exited_east'
                        time.sleep(node_headway_seconds)
                        break

            if veh.destination == 'south':
                if incoming[0].ID == veh.ID:
                    incoming.pop(0)
                    Exited_south.vehicles.append(veh.ID)
                    Exited_south.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                    #print(f"For {veh.origin} to {veh.destination}\n")
                    print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) exited to (right turn) south at time {Exited_south.time}")
                    veh.current_node = 'Right_Exited_South'
                    time.sleep(node_headway_seconds)
                    break
        

        #incoming.pop(0)

        # Check if all vehicles have been processed
        if not incoming:
            break

#Yield_IM(queue_order_NSEW)
# def thread_save(queue, stop_event):
#     start_time = time.time()
#     direction = get_queue_name(queue)  # For title
#     filename = f'{direction}.csv'

#     with open(filename, 'w', newline='') as csvfile:
#         fieldnames = ['Vehicle ID', 'Time to Reach', 'Origin', 'Current Node', 'Destination']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()

#         # Create a set to store the IDs of vehicles already written
#         written_vehicle_ids = set()

#         while not stop_event.is_set():
#             # Check if the elapsed time is greater than 2 minutes (120 seconds)
#             if time.time() - start_time > 120:
#                 stop_event.set()
#                 break

#             # Write vehicle data row by row
#             for vehicle in queue:
#                 # Check if the vehicle ID has not been written before
#                 if vehicle.ID not in written_vehicle_ids:
#                     writer.writerow({
#                         'Vehicle ID': vehicle.ID,
#                         'Time to Reach': vehicle.time_to_reach_intersection,
#                         'Origin': vehicle.origin,
#                         'Current Node': vehicle.current_node,
#                         'Destination': vehicle.destination
#                     })
#                     # Add the vehicle ID to the set of written IDs
#                     written_vehicle_ids.add(vehicle.ID)

#             # Sleep for some time before saving data again
#             time.sleep(2)  # Adjust the sleep time according to your needs

# Create a dictionary to store sets of unique current_node values for each vehicle
unique_current_nodes = {vehicle.ID: set() for queue in all_queues for vehicle in queue}


def save_vehicle_data(queue):
    global unique_current_nodes
    #print("#####################", unique_current_nodes)
    direction = get_queue_name(queue)  # For title
    filename = f'{direction}.csv'
    # dummy_data = [
    #     {'Vehicle ID': 7, 'Time to Reach': 10, 'Origin': 'A', 'Current Node': 'B', 'Destination': 'C'},
    #     {'Vehicle ID': 8, 'Time to Reach': 20, 'Origin': 'B', 'Current Node': 'C', 'Destination': 'D'},
    #     {'Vehicle ID': 9, 'Time to Reach': 15, 'Origin': 'C', 'Current Node': 'D', 'Destination': 'E'},
    #     # Add more dummy data rows as needed
    # ]
    with open(filename, 'a', newline='') as csvfile:
        
        fieldnames = ['Vehicle ID', 'Time to Reach', 'Origin', 'Current Node', 'Destination']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
     
        while True:
            # Check if there are any changes in the vehicles' current_node values
            data_changed = False
            for vehicle in queue:
                #print("#####################", unique_current_nodes[vehicle.ID])
                if vehicle.current_node not in unique_current_nodes[vehicle.ID]:
                    # print("\n########", vehicle.origin)
                    # for data_row in dummy_data:
                        # writer.writerow(data_row)
                        
                    writer.writerow({
                        'Vehicle ID': vehicle.ID,
                        'Time to Reach': vehicle.time_to_reach_intersection,
                        'Origin': vehicle.origin,
                        'Current Node': vehicle.current_node,
                        'Destination': vehicle.destination
                    })
                    csvfile.flush()
                    # Add the current_node value to the set of unique current_node values for this vehicle
                    unique_current_nodes[vehicle.ID].add(vehicle.current_node)
                    data_changed = True

            # If there were no changes in the data, sleep for a short time before checking again
            #if not data_changed:
                    time.sleep(1)  # Adjust the sleep time according to your needs
##########################################
    

# Create and start the thread for saving queue data
queues_to_save = {
        'SR': SR,
        'SL': SL,
        'NO': NO,
        'NR': NR,
        'NL': NL,
        'EO': EO,
        'ER': ER,
        'EL': EL,
        'WO': WO,
        'WR': WR,
        'WL': WL,

        'SS': SS,
        'NS': NS,
        'ES': ES,
        'WS': WS}



# Define a function to check if NSEW has 10 or more vehicles
def check_NSEW_length():
    return len(queue_order_NSEW) >= 10

# Function to run random_NSEWvehicle_REQUESTS, arrange_vehicle_requests_by_time, and Yield_IM (STORAGE ZONE)
def thread_populating():
    #start_time = time.time()

    while not check_NSEW_length():
    # while not stop_event.is_set():
    #     # Check if the elapsed time is greater than 2 minutes (120 seconds)
    #     if time.time() - start_time > 60:
    #         stop_event.set()
    #         break   
        random_NSEWvehicle_REQUESTS() #vehicles
        arrange_vehicle_requests_by_time(queue_order_NSEW) #IM
        #Yield_IM(queue_order_NSEW)
        #handle_emergency_vehicle()
        #time.sleep(1)



# Wait for the populating thread to finish (You can set a timeout or use a signal handler to stop the thread gracefully)
#populating_thread.join()

#stop_event=threading.Event()

# Create and start the thread for populating
populating_thread = threading.Thread(target=thread_populating)
populating_thread.start()

#to save and join all threads
all_thread=[]
thread_N_S = threading.Thread(target=define_Nodes, args=(NO,))
thread_N_S.start()


thread_N_E = threading.Thread(target=define_Nodes, args=(NL,))
thread_N_E.start()


thread_N_W = threading.Thread(target=define_Nodes, args=(NR,))
thread_N_W.start()

# From South

thread_S_N = threading.Thread(target=define_Nodes, args=(SO,))
thread_S_N.start()


thread_S_E = threading.Thread(target=define_Nodes, args=(SR,))
thread_S_E.start()

thread_S_W = threading.Thread(target=define_Nodes, args=(SL,))
thread_S_W.start()

# From east

thread_E_S = threading.Thread(target=define_Nodes, args=(EL,))
thread_E_S.start()


thread_E_N = threading.Thread(target=define_Nodes, args=(ER,))
thread_E_N.start()


thread_E_W = threading.Thread(target=define_Nodes, args=(EO,))
thread_E_W.start()

# From west

thread_W_S = threading.Thread(target=define_Nodes, args=(WR,))
thread_W_S.start()

thread_W_E = threading.Thread(target=define_Nodes, args=(WO,))
thread_W_E.start()


thread_W_N = threading.Thread(target=define_Nodes, args=(WL,))
thread_W_N.start()





# def update_vehicle_time_lost(queue, time_lost):
#     for vehicle in queue:
#         vehicle.time_to_reach_intersection += time_lost

# def dequeue_and_append_toadj(source_queue, dest_queue, num_vehicles, time_lost=1, time_reenter=1):
#     dequeued_vehicles = []
#     for vehicle in source_queue:
#         source_queue.pop(0)
#         vehicle.time_to_reach_intersection += time_lost
#         dequeued_vehicles.append(vehicle)
#     # insert elements from the dequeued_vehicles list, at the beginning of the dest_queue
#     dest_queue[:0] = dequeued_vehicles

# #dequeue_and_append_toadj(SO, NO, 3)
# #####dest
# def prioritize_queue_vehicle_request_from_origin(queue, time_lost=1, time_reenter=1):
#     if any(vh.ID.startswith('emergency') for vh in queue):
#         for index, vh in enumerate(queue):
#             if vh.ID.startswith('emergency'):
#                 priority_vehicle = queue.pop(index)
#                 queue.insert(0, priority_vehicle)
#                 break

#         next_queue = get_next_queue(queue)
#         if next_queue is not None:
#             num_vehicles_to_move = min(len(queue), len(next_queue))
#             dequeue_and_append_toadj(queue, next_queue, num_vehicles_to_move, time_lost, time_reenter)

# def get_next_queue(queue):
#     origin_prefix = queue[0].origin[0].upper()
#     destination_prefix = queue[0].destination[0].upper()

#     if destination_prefix == 'S':
#         if origin_prefix == 'N':
#             return SO
#         elif origin_prefix == 'E':
#             return SR
#         elif origin_prefix == 'W':
#             return SL
#     elif destination_prefix == 'N':
#         if origin_prefix == 'S':
#             return NO
#         elif origin_prefix == 'E':
#             return NR
#         elif origin_prefix == 'W':
#             return NL
#     elif destination_prefix == 'E':
#         if origin_prefix == 'N':
#             return EO
#         elif origin_prefix == 'S':
#             return ER
#         elif origin_prefix == 'W':
#             return EL
#     elif destination_prefix == 'W':
#         if origin_prefix == 'N':
#             return WO
#         elif origin_prefix == 'S':
#             return WR
#         elif origin_prefix == 'E':
#             return WL


