'''
Created on Sep 18, 2021
Updated on Sep 23, 2021
@author: Nodever2
'''

'''##########################################
############ Beginning of config ############
##########################################'''
ConfigMaxHumansPerGame = 6#Default: 6. Will change to default if not set to an int between 1 and 6 (inclusive).
#todo: add optional alternate algorithm for RNGing what team players are on that has an equal chance of all open slots
#also make it so that the names of maps/leaders print with spaces instead of underscores if possible?
'''##########################################
############### End of config ###############
##########################################'''

import random
import math
from enum import Enum

class HWLeader(Enum):#Enum with all possible leaders in Halo Wars
    INVALID = 0#except this
    The_United_Rebel_Front = 1
    The_Flood_Gravemind = 2
    Sesa_Refumee = 3
    The_Grunt_Rebellion = 4
    Captain_Cutter = 5
    Sergeant_Forge = 6
    Professor_Anders = 7
    Arbiter = 8
    Tartarus = 9
    Prophet_Of_Regret = 10
    
class HWMap(Enum):#Enum with all possible maps in Halo Wars
    INVALID = 0#except this
    BLOOD_GULTCH = 1#1v1
    CHASMS = 2
    PIRTH_OUTSKIRTS = 3
    RELEASE = 4
    TUNDRA = 5
    BARRENS = 6
    BLOOD_RIVER = 7
    BEASLEYS_PLATEAU = 8#2v2
    CREVICE = 9
    THE_DOCKS = 10
    LABYRINTH = 11
    REPOSITORY = 12
    TERMINAL_MORAINE = 13
    MEMORIAL_BASIN = 14
    EXILE = 15#3v3
    FORT_DEEN = 16
    FROZEN_VALLEY = 17
    GLACIAL_RAVINE = 18

'''
* HWError: function that displays error/warning message and terminates program if needed.
* @param str errormsg: A string, the error message to be displayed.
* @param int isError: 1 if error and program should be terminated, 0 if warning.
'''
def HWerror(errormsg, isError):
    if (not(isinstance(isError, int)) or (isError < 0) or (isError > 1)):
        print("Error or warning encountered. Invalid error flag, should be 1 if error, 0 if warning. Terminating.")
        isError = 1
    if (isinstance(errormsg, str)):
        print(errormsg)
    else:
        print("Error or warning encountered. Invalid error message.")
    if (isError == 1):
        print()
        input("Press enter to close...")
        exit()


'''##########################################
############ Beginning of script ############
##########################################'''
#STEP 1: INPUT    
pcInput = input("How many players? ")

#STEP 2: INITIALIZATION OF CORE VARIABLES
#        AND ERROR CHECKING ON CONFIG AND INPUT
try:
    humanCount = int(pcInput)
except ValueError:
    HWerror("Unexpected input. Terminating.", 1)

if (humanCount <= 0):
    HWerror("Unexpected input. Terminating.", 1)

if (not(isinstance(ConfigMaxHumansPerGame,int))):
    HWerror("Config Error: Max Humans Per Game is not an integer. Terminating.", 1)
    
maxHumans = 6
if (ConfigMaxHumansPerGame >= 1 and ConfigMaxHumansPerGame <= 6):
    maxHumans = ConfigMaxHumansPerGame
else:
    HWerror("Config Warning: Max Humans Per Game is outside the allowed range. Using " + str(maxHumans) + " instead.", 0)

numGamesLeft = int(math.ceil(humanCount/maxHumans))#pre-calculated, later used to determine how many humans in each game
remainingUnallocatedHumans = humanCount#keeps track of how many players there are left to allocate
iteration = 0#this is used to display game #
currentHumanIndex = 0#global index into randomizedHumanArray

#STEP 3: RANDOMIZE THE PLAYER ORDER
#This algorithm uses the Fisher-Yates shuffle. See https://bost.ocks.org/mike/shuffle/ for more info.
randomizedHumanArray = [(i+1) for i in range(humanCount)]
for i in range(humanCount):
    randomEntry = random.randint(i,humanCount-1)
    temp = randomizedHumanArray[i]
    randomizedHumanArray[i] = randomizedHumanArray[randomEntry]
    randomizedHumanArray[randomEntry] = temp
    
#STEP 4: ITERATE THROUGH EACH GAME
while (remainingUnallocatedHumans > 0):
    #STEP 4.1: SETUP AND CALCULATE HOW MANY HUMANS THIS GAME WILL HAVE
    print()#print an empty line for aesthetics.
    iteration = iteration + 1                                            
    print("===========================")
    print("GAME " + str(iteration) + ": ")
    humansThisGame = -1
    if (remainingUnallocatedHumans > maxHumans):
        humansThisGame = int(math.ceil(remainingUnallocatedHumans/numGamesLeft))     #amount of players in each game (todoL figure this out before the loop I think)
    else:
        humansThisGame = remainingUnallocatedHumans
    remainingUnallocatedHumans -= humansThisGame
    
    #STEP 4.2: RANDOMIZE TEAM SIZE (1v1, 2v2, or 3v3)
    teamSize = -1
    if (humansThisGame <= 2):
        teamSize = random.randint(1,3)
    elif (humansThisGame <= 4):
        teamSize = random.randint(2,3)
    else:
        teamSize = 3
    print("  This game will be a " + str(teamSize) + "v" + str(teamSize))
    
    #STEP 4.3: RANDOMIZE MAP BASED ON TEAM SIZE
    mapThisGame = HWMap(0)#default: invalid map
    if (teamSize == 1):
        mapThisGame = HWMap(random.randint(1,18))
    elif (teamSize == 2):
        mapThisGame = HWMap(random.randint(8,18))
    else:#3v3
        mapThisGame = HWMap(random.randint(15,18))
    print("  MAP: " + str(mapThisGame.name))
    
    #STEP 4.4: RANDOMIZE WHICH TEAM EACH HUMAN IS ON
    rows, cols = (teamSize*2, 2)                                    #initialize the player array according to team size (and thus # of players in game)
    arr = [[0 for i in range(cols)] for j in range(rows)]#array, where index = player number, 1st value = [(human ID) if human, 0 if AI], 2nd value = leader ID [1-10] (note that AIS can never have 1 here)
    for i in range(humansThisGame):                        #assign each human a slot in array.
        desiredSlot = random.randint(0,1)*teamSize
        while (arr[desiredSlot][0] != 0):
            desiredSlot = desiredSlot + 1
            if (desiredSlot >= rows):
                desiredSlot = 0
        arr[desiredSlot][0] = randomizedHumanArray[currentHumanIndex]#player # = random human ID (this array is pre-randomized)
        currentHumanIndex = currentHumanIndex + 1
    
    #STEP 4.5: RANDOMIZE WHICH LEADER EACH PLAYER WILL BE (AIs are players too)
    for i in range(rows):#RNG each player's leader
        if (arr[i][0] != 0):#if a human player is in this slot
            arr[i][1] = HWLeader(random.randint(1,10))
        else:#if an AI player is in this slot (AIs cannot play as the United Rebel Front in this game)
            arr[i][1] = HWLeader(random.randint(2,10))
    
    #STEP 4.6: PRINT RESULTS. FIX SPACING TO DYNAMICALLY RESIZE OUTPUT BASED ON NUMBER OF PLAYERS USING str.rjust().
    for i in range((int)(rows)):
        if (i == 0):
            print("  TEAM ALPHA:")
        elif(i == (int)(rows/2)):
            print("  TEAM BRAVO:")
        if (arr[i][0] != 0):
            print("    Player " + str(arr[i][0]).rjust(len(str(humanCount)),' ') + ": " + str(arr[i][1].name))
        else:
            print("    AI     " + str().rjust(len(str(humanCount)),' ') + ": " + str(arr[i][1].name))
   
    #STEP 4.7: FINISH LOOP AND PREPARE VARIABLES FOR NEXT ITERATION.    
    numGamesLeft = numGamesLeft - 1
    
#STEP 5: END PROGRAM ONCE LOOP FINISHES
print()
input("Press enter to close...")