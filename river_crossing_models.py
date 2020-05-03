'''
Model classes / entities for river crossing program.
'''

from enum import Enum

class Node:
    '''
    Represents a node in the tree that holds all possible state transitions.
    '''

    def __init__(self, state, rightPath=False):
        self.state = state
        self.children = []
        self.rightPath = rightPath
        self.riders = []

    def addChild(self, childState, riders):
        child = Node(childState)
        child.setRiders(riders)
        self.children.append(child)

    def getChildren(self):
        return self.children

    def getState(self):
        return self.state

    def markAsRightPath(self):
        '''
        Indicates this node is a valid step towards the target.
        '''
        self.rightPath = True

    def isRightPath(self):
        return self.rightPath

    def setRiders(self, riders):
        self.riders = riders

    def getRiders(self):
        return self.riders

    def __repr__(self):
        return "Missionaries: {}, Cannibals: {}".format(self.state.getMissionariesCount(), self.state.getCannibalsCount())

class RiverBank(Enum):
    '''
    Enum representing either banks of the river.
    '''

    ORIGIN = 0
    DESTINATION = 1

    def __str__(self):
        return self.name


class Riders(Enum):
    '''
    Enum representing the boat riders.
    '''

    Missionary = 0,
    Cannibal = 1

    def __str__(self):
        return self.name


class State:
    '''
    Representing the state values at the origin bank for a given node in the state transition tree.
    '''

    def __init__(self, missionariesCount, cannibalsCount, boatLocation=RiverBank.ORIGIN):
        # Valid states respecting the rule that the cannibals should not outnumber the missionaries.
        # Touple represents the missionary count and cannibal count respectively.
        validStates = {(3, 3), (3, 2), (3, 1), (3, 0), (2, 2),
                       (1, 1), (0, 0), (0, 1), (0, 2), (0, 3)}
        combination = (missionariesCount, cannibalsCount)

        if combination in validStates:
            self.missionariesCount = missionariesCount
            self.cannibalsCount = cannibalsCount
            self.boatLocation = boatLocation
        else:
            raise Exception(
                f"Impossible state. missionariesCount: {missionariesCount}, cannibalsCount: {cannibalsCount}")

    def __eq__(self, other):
        if isinstance(other, State):
            return self.missionariesCount == other.missionariesCount and self.cannibalsCount == other.cannibalsCount and self.boatLocation == other.boatLocation

        return False

    def __hash__(self):
        return hash(self.missionariesCount) + hash(self.cannibalsCount) + hash(self.boatLocation)

    def getMissionariesCount(self):
        return self.missionariesCount

    def getCannibalsCount(self):
        return self.cannibalsCount

    def getBoatLocation(self):
        return self.boatLocation
