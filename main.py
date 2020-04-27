'''
Core business logic of helping 3 missionaries and 3 cannibals to cross the river.
Problem Summary:
    Three missionaries and three cannibals come to a river and find a boat that holds two people.
    Everyone must get across the river to continue on the journey. 
    However, if the cannibals ever outnumber the missionaries on either bank, the missionaries will be eaten.
'''

from river_crossing_models import Node, Riders, RiverBank, State

def calculateTravelOptions(rootNode, desiredState):
    '''
    Calculate the travel options starting from the intial state, aka, rootNode.
    '''
    pathFound = findNextTravelOptions(rootNode, desiredState, set())
    if pathFound:
        rootNode.markAsRightPath()


def findNextTravelOptions(node, desiredState, tried):
    '''
    Find the next set of travel options for a given node.
    Recusrively do it until the desired state is reached.
    Desired state is when all the missionaries and cannibals have successfully crossed the river.
    '''

    tried.add(node.getState())
    state = node.getState()
    if state == desiredState:
        return True

    nextStatesAndRiders = generateChildren(state)

    for newStateAndRiders in nextStatesAndRiders:
        newState = newStateAndRiders[0]
        rideOption = newStateAndRiders[1]
        if newState not in tried:
            node.addChild(newState, rideOption)

    for childNode in node.getChildren():
        if findNextTravelOptions(childNode, desiredState, tried):
            childNode.markAsRightPath()
            return True

def generateChildren(state):
    '''
    Generate the next possible states from a given state.
    '''

    # Valid possiblities of riders in a boat trip.
    rideOptions = [
        [Riders.Missionary],
        [Riders.Missionary, Riders.Missionary],
        [Riders.Cannibal],
        [Riders.Cannibal, Riders.Cannibal],
        [Riders.Missionary, Riders.Cannibal]
    ]
    statesAndRiders = []
    if state.getBoatLocation() == RiverBank.ORIGIN:
        for rideOption in rideOptions:
            # When boat is at the origin, a ride will reduce the number of people at the origin bank, Hence subtract.
            missionariesCount = state.getMissionariesCount() - rideOption.count(Riders.Missionary)
            cannibalsCount = state.getCannibalsCount() - rideOption.count(Riders.Cannibal)
            try:
                newState = State(missionariesCount,
                                 cannibalsCount, RiverBank.DESTINATION)
                statesAndRiders.append((newState, rideOption))
            except Exception:
                pass
    elif state.getBoatLocation() == RiverBank.DESTINATION:
        for rideOption in rideOptions:
            # When boat is at the destination, a ride will increase the number of people at the origin bank, Hence perform addition.
            missionariesCount = state.getMissionariesCount() + rideOption.count(Riders.Missionary)
            cannibalsCount = state.getCannibalsCount() + rideOption.count(Riders.Cannibal)
            try:
                newState = State(missionariesCount,
                                 cannibalsCount, RiverBank.ORIGIN)
                statesAndRiders.append((newState, rideOption))
            except Exception:
                pass

    return statesAndRiders


def printPath(node):
    '''
    Recursively print the series of actions/rides performed to transport the missionaries and cannibals abiding the rules.
    '''

    print("=========================================================\n")
    if node.getRiders():
        print(f"A {' and a '.join(str(rider) for rider in node.getRiders())} riding to {node.getState().getBoatLocation()}\n")

    print(f"\tBoat is now at: {node.getState().getBoatLocation()}")
    print(f"\tOrigin Bank State: {node}")
    for child in node.getChildren():
        if child.isRightPath():
            printPath(child)


def main():
    '''
    Main driver of the logic to transport missionaries and cannibals.
    '''

    missionariesAtOrigin = 3
    cannibalsAtOrigin = 3
    initialBoatLocation = RiverBank.ORIGIN

    # In the intial state, the boat, 3 missionaries, and 3 cannibals are at the Origin bank of the river.
    initialState = State(missionariesAtOrigin,
                         cannibalsAtOrigin, initialBoatLocation)

    desiredMissionariesAtOrigin = 0
    desiredCannibalsAtOrigin = 0
    finalBoatLocation = RiverBank.DESTINATION

    # In the desired/target state, the boat, 3 missionaries, and 3 cannibals are at the Destination bank of the river.
    desiredState = State(desiredMissionariesAtOrigin,
                         desiredCannibalsAtOrigin, finalBoatLocation)

    rootNode = Node(initialState, True)
    calculateTravelOptions(rootNode, desiredState)
    printPath(rootNode)


main()
