# Kirby Little Game Turn based v 0.01

# StanderSam

###################################################

# Player Class

import time
import os



class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()

class GameState:
    def __init__(self):
        self.turnCount = 0
    def turnPlus(self):
        self.turnCount +=1
    def currentTurnCount(self):
        return self.turnCount
    def reset(self):
        self.turnCount = 0

class Ability:
    def __init__(self, name, ID, moveListID):
        self.name = name
        self.ID = ID
        self.moveListID = moveListID

    def printMoves(self):
        for i in moveListID:
            i.display()
        pass


class Moves:
    def __init__(self, 
    name, 
    hotkey, 
    ability, 
    abilityID,
    ID,
    power = 0,
    cost = 0,
    atkRange = (0,0), 
    defense = 0, 
    cooldown = 0,
    continuousUse = 0, 
    movement = 0, 
    universal = 0, 
    attackTimes = 1, 
    piercing = 0, 
    lingeringTurns = 0, 
    forcedNextMoveID = -1,
    moveLock = 0,
    airborne = 0,
    specialState = 0):
        self.name = name
        self.hotkey = hotkey
        self.ability = ability
        self.abilityID = abilityID
        self.ID = ID # Move ID
        self.power = power # Move Power
        self.cost = cost # Energy cost
        self.atkRange = atkRange # (0,0) = (From this height relative to player, To this height ...)
        self.defense = defense # Defense Power
        self.cooldown = cooldown # How many turns this move cannot be selected after continuousUse
        self.continuousUse = continuousUse # -1 = can use infinite amount of time, number = can use a number of times continuously
        self.movement = movement # Positive value increase height, Negative decrease height
        self.universal = universal # If the move is a universal move
        self.attackTimes = attackTimes # Multi Attack deals attackTimes x power damage, but gets pierced by higher attack
        self.piercing = piercing # Damage if defended
        self.lingeringTurns = lingeringTurns # If it lingers like a cutter throw
        self.forcedNextMoveID = forcedNextMoveID # If the move have a forced next move
        self.moveLock = moveLock # 0 = can be used anytime; 1 = locked until certain criteria is met (Passive); 2 = Can only be forced into.
        self.airborne = airborne # 0 = can be used whenever, 1 = can only be used when airborne, 2 = can only be used grounded
        self.specialState = specialState # Special Counter for things like Stone mode

        

    def reset(self):
        self.name = "None"
        self.hotkey = ''
        self.ability = "None"
        self.abilityID = 0
        self.ID = -1
        self.power = 0
        self.cost = 0
        self.atkRange = (0, 0)
        self.defense = 0
        self.cooldown = 0 # How many turns this move cannot be selected after continuousUse
        self.continuousUse = -1 # -1 = can use infinite amount of time, number = can use a number of times continuously
        self.movement = 0 # Positive value increase height, Negative decrease height
        self.universal = True # If the move is a universal move
        self.attackTimes = 1 # Multi Attack deals attackTimes x power damage, but gets pierced by higher attack
        self.piercing = 0 # Damage if defended
        self.lingeringTurns = 0 # If it lingers like a cutter throw
        self.forcedNextMoveID = -1 # If the move have a forced next move
        self.moveLock = 0 # 0 = can be used anytime; 1 = locked until certain criteria is met (Passive); 2 = Can only be forced into.
        self.airborne = 0
        self.specialState = 0 #   
        
    def simplePrint(self):
        print("\""+ self.name +
        "\" Hotkey: " + self.hotkey + 
        "Power: " + self.power +
        "Cost: " + self.cost + "\n" )

    def display(self):
        print("Move Name: \""+ self.name +
        "\" Hotkey: " + self.hotkey + "\n" )

        if (self.power!=0):
            print(" Power: " + str(self.power))
            
            if(self.atkRange == (-99, 0)):
                print(" Hits everything below you, including your current level. ")
            elif(self.atkRange == (0, 99)):
                print(" Hits everything above you, including your current level. ")
            elif(self.atkRange == (-99, -1)):
                print(" Hits everything below you, excluding your current level. ")
            elif(self.atkRange == (1, 99)):
                print(" Hits everything above you, excluding your current level. ")
            else:
                print(" Range: " + str(self.atkRange))

        if (self.defense !=0):
            print(" Armor: " + str(self.defense) + "\n")

        print(" Energy Cost: " + str(self.cost))
        

        if (self.continuousUse != 0):
            print(" Can be used " + str(self.continuousUse) + 
            " times continuously, then you have to wait " + str(self.cooldown) + 
            " turns to use it again.\n")
        

        if (self.movement != 0):
            if self.movement > 0:
                print(" Move up " + str(self.movement) + " level.\n" ) 
            else:
                if(self.movement == -99):
                    print(" Move down to the ground level.\n" )
                else:
                    print(" Move down " + str(self.movement * -1) + " level.\n" )

        if (self.attackTimes != 1):
            print(" Attack " + str(self.attackTimes) + " times.\n")

        if (self.piercing != 0):
            print(" Ignores Defend; Does " + str(self.piercing) + " damage if defended." + "\n")

        if (self.lingeringTurns != 0): # If it lingers like a cutter throw
            print(" Lingers for the next " + str(self.lingeringTurns) + " turns.\n" )
        
        if(self.forcedNextMoveID != -1):
            print(" Next move has to be \"" + Global_MoveNameList[findMoveIndex(self.forcedNextMoveID)] + "\".\n")

        if(self.airborne == 1):
            print(" Can only be used in the air." )

        if(self.airborne == 2):
            print(" Can only be used on the ground." )

        if(self.moveLock == 1):
            print(" Cannot be used, unless a certain condition is met.\n")
        elif(self.moveLock == 2):
            print(" Cannot be used, unless forced into.\n")

        print("\n")

# Various memory for one player
class Counter:
# 0th counter: Defend Times

    def __init__(self, number):
        self.counters = [0] * number

    def changeDelta(self, counterNum, delta):
        self.counters[counterNum] = self.counters[counterNum] + delta

    def changeTo(self, counterNum, num):
        self.counters[counterNum] = num

    def getCounter(self, counterNum):
        return self.counters[counterNum]

    def reset(self, number):
        self.counters = [0] * number

class Player:

    def __init__(self, ID, abilityID, human=True):
        self.ID = ID
        self.abilityID = abilityID
        self.HP = 100
        self.energy = 0
        self.height = 0
        self.human = human
        self.forcedMove = -1
        self.state = 0
        self.counter = Counter(1)
        self.moveIDHistory = []
        self.allowedMoveIDList = []
    
    def __str__(self):
        return("Player " + str(self.ID) + ": " + str(self.abilityID) + " HP: " + str(self.HP) +"\n" + " Energy: " + str(self.energy) +"\n Height: " + str(self.height) + "\n")
    
    def reset(self):
        self.ID = 0
        self.abilityID = 0
        self.HP = 100
        self.energy = 0
        self.height = 0
        self.forcedMove = -1
        self.state = 0
        self.counter = Counter(1)
        self.moveIDHistory = []
        self.allowedMoveIDList = []
    

def loadAbility():
    AbilityList = []
    AbilityNameList = []

    ability_None_0 = Ability("None", 0, [0,1,2,3])
    ability_Sword_1 = Ability("Sword", 1, [0,1,2,3, 100, 101, 102, 103, 104, 105])
    ability_Cutter_2 = Ability("Cutter", 2, [0,1,2,3, 201, 203, 205, 206, 207, 208])
    ability_Hammer_3 = Ability("Hammer", 3, [0,1,2,3, 300, 301, 302, 303, 304])
    ability_Tornado_4 = Ability("Tornado", 4, [0,1,2,3, 400, 401, 402, 403, 404, 405])
    ability_Master_5 = Ability("Master", 5, [0,1,2,3, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511])

    AbilityList=[ability_None_0, ability_Sword_1, ability_Cutter_2, ability_Hammer_3, ability_Tornado_4, ability_Master_5]
    
    for ability in AbilityList:
        AbilityNameList.append(ability.name)
    return AbilityList, AbilityNameList

def loadMoves():
    MoveList = []
    

    move_None_neg1 = Moves("None", '  ', "None", 0, -1, power=0, cost = 1)

    # Naming: move_A(Air)/B(Both)/G(Ground)_NameAlias_MoveID

    # Universal Moves
    move_B_Charge_0 = Moves("Charge", 'q', "None", 0, 0, power=0, cost=-1, universal=1, airborne = 0)
    move_B_Fly_1 = Moves("Fly", 'f', "None", 0, 1, power = 0, universal = 1, movement=1, airborne = 0)
    move_A_Drop_2 = Moves("Drop", 'd', "None", 0, 2, power=0, universal = 1, movement=-1, airborne = 1)
    move_G_Defend_3 = Moves("Defend", 'w', "None", 0, 3, power=0, universal = 1, defense=1000, cooldown= 1, continuousUse=2, airborne = 2)

    # Sword Moves 
    move_Sword_G_BasicATK_100 = Moves("Slash", 'e', "Sword", 1, 100, power = 100, cost=1, atkRange=(0,0), airborne = 2)
    move_Sword_A_BasicATK_101 = Moves("Spin Slash", 'e', "Sword", 1, 101, power = 100, cost=1, atkRange=(0,0), airborne = 1)
    move_Sword_G_SuperBigATK_102 = Moves("Final Slash", 'y', "Sword", 1, 102, power = 300, cost=4, atkRange=(0,0), airborne = 2, piercing=100)
    move_Sword_G_LargeATK_103 = Moves("Dash Slash", 'r', "Sword", 1, 103, power = 200, cost=2, atkRange=(0,0), airborne = 2)
    move_Sword_B_RisingATK_104 = Moves("Rising Slash", 't', "Sword", 1, 104, power = 300, cost=3, atkRange=(0,1), airborne = 0, forcedNextMoveID=105, movement= 1)
    move_Sword_C_A_DroppingATK_105 = Moves("Dropping Slash", 't', "Sword", 1, 105, power = 100, cost=0, atkRange=(-99,0), airborne = 1, movement= -99, piercing = 100, moveLock = 2)

    # Cutter Moves
    # move_Cutter_B_BoomUp_200
    move_Cutter_B_BoomCurr_201 = Moves("Cutter Boomerang (Straight)", 'r', "Cutter", 2, 201, power = 50, cost=1, atkRange=(0,0), airborne = 0, lingeringTurns = 1)
    # move_Cutter_B_BoomDown_202
    move_Cutter_G_LargeATK_203 = Moves("Cutter Dash", 'y', "Cutter", 2, 203, power = 200, cost=2, atkRange=(0,0), airborne = 2)
    move_Cutter_A_DroppingATK_205 = Moves("Cutter Drop", 'i', "Cutter", 2, 205, power = 100, cost=2, atkRange=(-99,0), airborne = 1, movement = -99)
    move_Cutter_G_ComboATK0_206 = Moves("Cleaving Cutter", 'o', "Cutter", 2, 206, power = 50, cost=3, atkRange=(0,0), airborne = 2, movement = 0, forcedNextMoveID=207)
    move_Cutter_G_ComboATK1_207 = Moves("Non-Stop Cutter", 'o', "Cutter", 2, 207, power = 100, cost=0, atkRange=(0,1), airborne = 2, movement = 1, forcedNextMoveID=208, moveLock = 2)
    move_Cutter_A_ComboATK2_208 = Moves("Final Cutter", 'o', "Cutter", 2, 208, power = 200, cost=0, atkRange=(-99,0), airborne = 1, movement = -99, moveLock = 2)


    # Hammer Moves
    move_Hammer_G_BasicATK_300 = Moves("Hammer Nail", 'e', "Hammer", 3, 300, power = 150, cost=1, atkRange=(0,0), airborne = 2)
    move_Hammer_A_BasicATK_301 = Moves("Giant Swing", 'e', "Hammer", 3, 301, power = 150, cost=1, atkRange=(0,0), airborne = 1)
    move_Hammer_G_LargeATK_302 = Moves("Hammer Swing", 'r', "Hammer", 3, 302, power = 250, cost=2, atkRange=(0,0), airborne = 2)
    move_Hammer_G_SuperBigATK0_303 = Moves("Hammer Flip Charge", 't', "Hammer", 3, 303, power = 100, cost=3, atkRange=(0,0), airborne = 2, forcedNextMoveID=304)
    move_Hammer_G_SuperBigATK1_304 = Moves("Hammer Flip", 't', "Hammer", 3, 304, power = 500, cost=0, atkRange=(0,0), airborne = 2, moveLock = 2, piercing=200)
    
    # Tornado Moves
    move_Tornado_B_Tornado0_400 = Moves("Tornado Attack", 'e', "Tornado", 4, 400, power = 100, cost = 1, atkRange=(0,1), airborne = 0, defense = 100, forcedNextMoveID=401)
    move_Tornado_B_Tornado1_401 = Moves("Tornado Attack", 'e', "Tornado", 4, 401, power = 100, cost = 0, atkRange=(0,1), airborne = 0, defense = 100, forcedNextMoveID=402, moveLock = 2)
    move_Tornado_B_Tornado2_402 = Moves("Tornado Attack End", 'e', "Tornado", 4, 402, power = 0, cost = 0, atkRange=(0,0), airborne = 0, defense = 0, moveLock = 2)
    move_Tornado_B_UpAtk_403 = Moves("Rising Gust", 'r', "Tornado", 4, 403, power = 100, cost = 1, atkRange=(1, 2), airborne = 0, defense = 0)
    move_Tornado_B_DownAtk_404 = Moves("Falling Gust", 't', "Tornado", 4, 404, power = 100, cost = 1, atkRange=(-2, -1), airborne = 0, defense = 0)
    move_Tornado_A_LargeAtk_405 = Moves("Tornado Dash", 'y', "Tornado", 4, 405, power = 100, cost = 3, atkRange=(-1, 1), airborne = 1, defense = 100)

    # Master Moves
    move_Master_G_BasicATK_500 = Moves("Overhead Slash", 'e', "Master", 5, 500, power = 100, cost = 1, atkRange=(0,0), airborne = 2)
    move_Master_G_MultiATK_501 = Moves("MultiSword Attack", 'r', "Master", 5, 501, power = 50, cost = 1, atkRange=(0,0), airborne = 2, attackTimes = 6)
    move_Master_G_LargeATK_502 = Moves("Final Swing", 't', "Master", 5, 502, power = 200, cost = 2, atkRange=(0,0), airborne = 2)
    move_Master_G_BasicATK2_503 = Moves("Sword Stab", 'y', "Master", 5, 503, power = 80, cost = 1, atkRange=(0,0), airborne = 2, forcedNextMoveID=504)
    move_Master_G_ComboATK0_504 = Moves("Final Cutter", 'y', "Master", 5, 504, power = 200, cost = 0, atkRange=(0,1), airborne = 2, moveLock = 2, forcedNextMoveID=505, movement = 1, defense = 1000)
    move_Master_A_ComboATK1_505 = Moves("Final Cutter", 'y', "Master", 5, 505, power = 100, cost = 0, atkRange=(-99,0), airborne = 1, moveLock = 2, defense=1000, movement = -99, piercing=100)
    move_Master_B_UpAtk_506 = Moves("Up Thrust", 'u', "Master", 5, 506, power = 100, cost = 1, atkRange=(1, 1), airborne = 0)
    move_Master_A_DownAtk_507 = Moves("Down Thrust", 'i', "Master", 5, 507, power = 100, cost = 1, atkRange=(-99, -1), airborne = 1, movement= -99)
    move_Master_B_SuperBigATK_508 = Moves("Drill Rush", 'o', "Master", 5, 508, power = 100, cost = 4, atkRange=(0,0), airborne = 0, piercing=100, attackTimes = 3)
    move_Master_A_BasicATK_509 = Moves("Sword Spin", 'r', "Master", 5, 509, power = 100, cost=1, atkRange=(0,0), airborne = 1)
    move_Master_B_ChargeATK0_510 = Moves("Crescent Shot Charge", 'p', "Master", 5, 510, power = 0, cost=1, atkRange=(0,0), airborne = 0, forcedNextMoveID=511)
    move_Master_B_ChargeATK1_511 = Moves("Crescent Shot", 'p', "Master", 5, 511, power = 200, cost=0, atkRange=(0,1), airborne = 0, moveLock = 2, piercing = 100)


    #######################################
    MoveList = [move_B_Charge_0,move_B_Fly_1, move_A_Drop_2, move_G_Defend_3,move_Sword_G_BasicATK_100,
     move_Sword_A_BasicATK_101, move_Sword_G_SuperBigATK_102, move_Sword_G_LargeATK_103,
      move_Sword_B_RisingATK_104, move_Sword_C_A_DroppingATK_105,
      move_Cutter_B_BoomCurr_201, move_Cutter_G_LargeATK_203, move_Cutter_A_DroppingATK_205,
      move_Cutter_G_ComboATK0_206, move_Cutter_G_ComboATK1_207, move_Cutter_A_ComboATK2_208,
      move_Hammer_G_BasicATK_300, move_Hammer_A_BasicATK_301,
      move_Hammer_G_LargeATK_302, move_Hammer_G_SuperBigATK0_303,
      move_Hammer_G_SuperBigATK1_304, 
      move_Tornado_B_Tornado0_400, move_Tornado_B_Tornado1_401, move_Tornado_B_Tornado2_402, 
      move_Tornado_B_UpAtk_403, move_Tornado_B_DownAtk_404, move_Tornado_A_LargeAtk_405,
      move_Master_G_BasicATK_500, move_Master_G_MultiATK_501,move_Master_G_LargeATK_502,
      move_Master_G_BasicATK2_503,move_Master_G_ComboATK0_504,move_Master_A_ComboATK1_505,move_Master_B_UpAtk_506,
      move_Master_A_DownAtk_507,move_Master_B_SuperBigATK_508, move_Master_A_BasicATK_509, 
      move_Master_B_ChargeATK0_510, move_Master_B_ChargeATK1_511

      ]

    MoveNameList = []
    for move in MoveList:
        MoveNameList.append(move.name)

    return MoveList, MoveNameList

class gameStatus:
    
    def __init__(self, P1, P2, _gameState):
        self.P1 = P1
        self.P2 = P2
        self.gameState = _gameState
        


    def display(self):
        print("Turn: " + str(self.gameState.currentTurnCount()))
        print("Player 1: Human\n") if self.P1.human else print("Player 1: CPU\n")
        print(" Ability: " + str(Global_AbilityNameList[self.P1.abilityID]) )
        print(" HP: " + str(self.P1.HP))
        print(" Energy: " + str(self.P1.energy))
        print(" Height: " + str(self.P1.height))
        if self.P1.forcedMove != -1: 
            print(" Forced into " + Global_MoveNameList[self.P1.forcedMove])
        print(" State: " + str(self.P1.state))
        print(" Defense Counter: " + str(self.P1.counter.counters[0]))
        print(" Move Log: ")
        for usedMoveIDs in self.P1.moveIDHistory:
            print(Global_MoveNameList[usedMoveIDs] + ", ")
        
        print(" Allowed Moves: ")
        for allowedMoveIDs in self.P1.allowedMoveIDList:
            print("   " + Global_MoveNameList[findMoveIndex(allowedMoveIDs)] + " ("+ str(Global_MoveList[findMoveIndex(allowedMoveIDs)].cost)  +"), ") if Global_MoveList[findMoveIndex(allowedMoveIDs)].cost >0 else print("   " + Global_MoveNameList[findMoveIndex(allowedMoveIDs)] + ", ")
        print("\n")

        print("Player 2: Human\n") if self.P2.human else print("Player 2: CPU\n")
        print(" Ability: " + str(Global_AbilityNameList[self.P2.abilityID] ))
        print(" HP: " + str(self.P2.HP))
        print(" Energy: " + str(self.P2.energy))
        print(" Height: " + str(self.P2.height))
        if self.P2.forcedMove != -1: 
            print(" Forced into " + Global_MoveNameList[self.P2.forcedMove])
        print(" State: " + str(self.P2.state))
        print(" Defense Counter: " + str(self.P2.counter.counters[0]))
        print(" Move Log: ")
        for usedMoveIDs in self.P2.moveIDHistory:
            print(Global_MoveNameList[usedMoveIDs] + ", ")

        print(" Allowed Moves: ")
        for allowedMoveIDs in self.P2.allowedMoveIDList:
            print("   " + Global_MoveNameList[findMoveIndex(allowedMoveIDs)] + " ("+ str(Global_MoveList[findMoveIndex(allowedMoveIDs)].cost)  +"), ") if Global_MoveList[findMoveIndex(allowedMoveIDs)].cost >0 else print("   " + Global_MoveNameList[findMoveIndex(allowedMoveIDs)] + ", ")
        print("\n")

        pass

    def moveAllowed(self, Player):

        possibleMoveListID = []
        for moveID in Global_AbilityList[Player.abilityID].moveListID:

            CostPass = False
            AirPass = False
            LockPass = False
            ForcedPass = False
            CoolDownPass = False
            SpecialStatePass = False

            moveIndex = -1

            # find move with that ID

            for i in range(len(Global_MoveList)):
                if Global_MoveList[i].ID == moveID:
                    moveIndex = i
                    break

            # Cost Sufficient?
            if(Player.energy >= Global_MoveList[moveIndex].cost):
                CostPass = True

            # In Air?
            if (Global_MoveList[moveIndex].airborne == 0 or Global_MoveList[moveIndex].airborne == 1 and Player.height > 0) or (Global_MoveList[moveIndex].airborne == 2 and Player.height <= 0):
                AirPass = True
            
            # Locked?
            if (Global_MoveList[moveIndex].moveLock == 0):
                LockPass = True
            elif (Global_MoveList[moveIndex].moveLock == 2): # Must be forced into
                if (Player.forcedMove == moveIndex):
                    LockPass = True
            
            # Not Forced?
            if (Player.forcedMove == -1 or Player.forcedMove == moveIndex):
                ForcedPass = True
            
            # CoolDown
            if(Global_MoveList[moveIndex].cooldown == 0):
                CoolDownPass = True
            elif(Global_MoveList[moveIndex].cooldown != 0):
                exceeded = False
                if (len(Player.moveIDHistory) > (Global_MoveList[moveIndex].continuousUse-1)):
                    
                    for i in range(Global_MoveList[moveIndex].cooldown):
                        if (len(Player.moveIDHistory) > (Global_MoveList[moveIndex].continuousUse-1 + Global_MoveList[moveIndex].cooldown)):
                            exceeded = True
                            if Player.moveIDHistory[-i-1] == moveID:
                                exceeded = True
                                for j in range(Global_MoveList[moveIndex].continuousUse-1):
                                    if Player.moveIDHistory[-i-2-j] != moveID:
                                        # This is fine; user did not exceed limit
                                        exceeded = False
                                if exceeded == True:
                                    break
                                else:
                                    continue # continue looking for continuous of move
                if exceeded == False:
                    CoolDownPass = True

            SpecialStatePass = True

            if(CostPass == AirPass == LockPass == ForcedPass == CoolDownPass == SpecialStatePass == True):
                possibleMoveListID.append(moveID)
           
            
        return possibleMoveListID
        
def findMoveIndex(moveID):
    moveIndex = -1

    # find move with that ID

    for i in range(len(Global_MoveList)):
        if Global_MoveList[i].ID == moveID:
            moveIndex = i
            return moveIndex

def gameLoop(P1, P2, _gameState):
    
    # Create game
    game = gameStatus(P1, P2, _gameState)
    # game loop

    while(1):

        # Update allowed moves
        game.P1.allowedMoveIDList = game.moveAllowed(game.P1)
        game.P2.allowedMoveIDList = game.moveAllowed(game.P2)
        game.gameState.turnPlus()

        print(game.P1)
        print(game.gameState.currentTurnCount())
        game.display()

        game.P1.energy += 5
        game.P1.allowedMoveIDList = game.moveAllowed(game.P1)
        game.P2.allowedMoveIDList = game.moveAllowed(game.P2)
        game.gameState.turnPlus()
        game.display()

        game.P1.height += 1
        game.P1.allowedMoveIDList = game.moveAllowed(game.P1)
        game.P2.allowedMoveIDList = game.moveAllowed(game.P2)
        game.gameState.turnPlus()
        game.display()

        for moveID in game.P1.allowedMoveIDList:
            moveIndex = -1

            # find move with that ID

            for i in range(len(Global_MoveList)):
                if Global_MoveList[i].ID == moveID:
                    moveIndex = i
                    break
            
            Global_MoveList[moveIndex].display()

        # Take in command

        
        
        # Test

        print("Game End!")
        break

        # Check if game end
        if(game.P1.HP <= 0 or game.P2.HP <= 0 ):
            print("Game End!")
            break
        #



        


    pass



def gameInit():

    global Global_AbilityList
    global Global_MoveList

    global Global_AbilityNameList
    global Global_MoveNameList

    Global_AbilityList=[]
    Global_MoveList = []

    Global_AbilityNameList=[]
    Global_MoveNameList = []

    P1 = Player(1, 0, human=True)
    P2 = Player(2, 0, human=True)
    gamestate = GameState()

    # Load Abilities

    Global_AbilityList, Global_AbilityNameList = loadAbility()
    Global_MoveList, Global_MoveNameList= loadMoves()

    # Ability Choosing
    cont = 1

    # P1
    if P1.human == True:
        while(cont == 1):
            print("Player 1! Choose an ability! Enter the full name of the ability.")

            ability = input().lower()

            if ability == "help":
                print ("Enter the full name of the ability. Current available abilities: ")
                for i in range(len(Global_AbilityList) - 1):
                    print (Global_AbilityList[i+1].name)

            else:
                # Check for ability
                for i in range(len(Global_AbilityList) - 1):
                    if ability == (Global_AbilityList[i+1].name.lower()):
                        P1.abilityID = Global_AbilityList[i+1].ID
                        cont = 0
                        break
    
    # P2
    if P2.human == True:
        cont = 1
        while(cont == 1):
            print("Player 2! Choose an ability! Enter the full name of the ability.")

            ability = input().lower()

            if ability == "help":
                print ("Enter the full name of the ability. Current available abilities: ")
                for i in range(len(Global_AbilityList) - 1):
                    print (Global_AbilityList[i+1].name)

            else:
                # Check for ability
                for i in range(len(Global_AbilityList) - 1):
                    if ability == (Global_AbilityList[i+1].name.lower()):
                        P2.abilityID = Global_AbilityList[i+1].ID
                        cont = 0
                        break

    # Game

    print("Start Game!")

    ##############################################

    gameLoop(P1, P2, gamestate)

    return 0

if __name__ == '__main__':
    gameInit()


