'''
Copyright [2022] [GamerTechUni]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''


import random
import sys

class Game:

        # A dictionary of caves and connections
        cave = {1:[2,5,8],
                2:[1,3,10],
                3:[2,4,12],
                4:[3,5,14],
                5:[1,4,6],
                6:[5,7,15],
                7:[6,8,17],
                8:[1,7,9],
                9:[8,10,18],
                10:[2,9,11],
                11:[10,12,19],
                12:[3,11,13],
                13:[12,14,20],
                14:[4,13,15],
                15:[6,14,16],
                16:[15,17,20],
                17:[7,16,18],
                18:[9,17,19],
                19:[11,18,20],
                20:[13,16,19]}
        

        # Player variables and threats
        def __init__(self):
                self.threats = {}
                self.arrows = 5
                self.player_location = -1
                self.game_over = False
                self.wump_dead = False
        
        def help():
                print("\nWelcome to 'Hunt the Wumpus'!")
                print("The objective of the game is to kill the wumpus, so you can win!")
                print("The wumpus is located in the 20 rooms of the cave, which is shaped like a dodecahedron")

                print("Hazards: \n")
                print("Bottomless pits:")
                print("There are two bottomless pits in the cave. If you move to a room with a bottomless pit,")
                print("you will fall into the pit and lose the game!")
                print("Super bats:")
                print("There are two super bat rooms in the cave. If you move to a room with super bats in it,")
                print("one of them will move you to another room, which could take you to a dangerous room!")
                print("Wumpus:")
                print("The wumpus does not care about hazards, as it has sucker feet, which allows it")
                print("to cling to walls in bottomless pits and is too heavy for super bats to lift up. The wumpus is")
                print("usually asleep. Two things wake up the wumpus: you shooting an arrow or moving into its room.")
                print("When the wumpus is awake, it will move to another room(25% chance),")
                print("or stay in its current room. If the wumpus is where you are after that, it will eat you")
                print("and you will lose the game!\n")
                print("You:")
                print("Each turn, you may move or shoot an crooked arrow")
                print("Moving: You can move one room through a connecting tunnel")
                print("You have five crooked arrows, named for their ability change direction during flight.")
                print("You lose the game when you run out of arrows.")
                print("Each arrow can travel up to five rooms. You aim by telling the program which rooms you want the")
                print("arrow to go to. If the arrow path is invalid, it will move to a random neighbouring room.")
                print("  If the arrow hits the wumpus, you win the game!")
                print("  If the arrow hits you, you lose the game!\n")
                print("Warnings:")
                print("When you are one room away from a threat, a warning will appear, which will say:")
                print("  Wumpus: I smell a wumpus nearby")
                print("  Super Bat: I hear bats nearby")
                print("  Pit: I feel a draft nearby\n")


        
        # Check if location is already taken 
        def search_threats(self, location):

                for threat in self.threats.values():

                        if threat == location:
                                return True
                        
                return False
        
        def general_search(my_list, location):

                for i in range(len(my_list)):
                        if my_list[i] == location:
                                return True

                return False

        def set_bat_rooms(self):
                bat1 = 0
                bat2 = 0
                while True:
                        bat1 = random.randint(1, 20)
                        bat2 = random.randint(1, 20)

                        if bat1 == bat2:
                                continue
                        else:
                                break
                
                self.threats["bat1"] = bat1
                self.threats["bat2"] = bat2
        
        def set_pit_rooms(self):
                pit1 = 0
                pit2 = 0
                while True:
                        pit1 = random.randint(1, 20)
                        pit2 = random.randint(1, 20)

                        if pit1 == pit2:
                                continue
                        
                        elif Game.search_threats(self, pit1) or Game.search_threats(self, pit2):
                                continue

                        else:
                                break

                self.threats["pit1"] = pit1
                self.threats["pit2"] = pit2
        
        def set_wump_room(self):
                wump = 0

                if self.player_location == -1:
                        while True:
                                wump = random.randint(1, 20)

                                if wump == self.player_location:
                                        continue

                                else:
                                        break
                else:
                        wump = random.choice(self.cave[self.threats['wump']])
                self.threats["wump"] = wump
        
        def set_player_spawn(self):
                while True:
                        self.player_location = random.randint(1, 20)

                        if Game.search_threats(self, self.player_location):
                                continue
                        else:
                                break
        
        def move_action(self):

                room_num = int(input("Which room do you want to move into?: "))

                if room_num not in Game.cave[self.player_location]:
                                print("You can not move to that room!")
                                return False
                else:
                        self.player_location = room_num
                        
                while True:

                        if self.player_location == self.threats["wump"]:
                                wump_chance = random.randint(1, 100)
                                if wump_chance > 25:
                                        print("\033[1mGame Over!: The wumpus ate you\033[0m")
                                        self.game_over = True
                                        break
                                elif wump_chance <= 25:
                                        print("You somehow scared wumpus away and caused it to move to another room!")
                                        #print(f"DEBUG: The wumpus room is now {self.threats['wump']}")
                                        Game.set_wump_room(self)
                                        continue

                        elif self.player_location == self.threats["bat1"] or self.player_location == self.threats["bat2"]:
                                print("A bat moved you to another room")
                                self.player_location = random.randint(1, 20)
                                continue
                        
                        elif self.player_location == self.threats["pit1"] or self.player_location == self.threats["pit2"]:
                                print("\033[1mGame Over!: You fell into a bottomless pit\033[0m")
                                self.game_over = True
                                break
                        else:
                                break
        
        def shoot_action(self):

                arrow_path = [self.player_location]
                try:
                        distance = int(input("Number of rooms(1-5, 0 - Not shooting): "))
                except ValueError:
                        print("That is not a valid number")
                        return False
                
                if distance < 0 or distance > 5:
                        print("Your arrow is not that crooked")
                        return False
                
                elif distance == 0:
                        return "not shooting"
                
                
                x = 0

                while x in range(distance):
                        try:
                                room = int(input("Room: "))
                        except ValueError:
                                print("That is not a valid number")
                                continue
                        arrow_path.append(room)
                        x += 1
                
                x1 = 1
                x2 = 0
                connecting_rooms = []
                valid_list = []

                invalid_path = False

                while x1 in range(len(arrow_path)):

                        connecting_rooms = self.cave[arrow_path[x2]]
                        #print(arrow_path[x2])
                        #print(f"DEBUG: Next room {arrow_path[x1]}")
                        #print(connecting_rooms)

                        for room in connecting_rooms:

                                if room == arrow_path[x1]:
                                        #print("DEBUG: Valid")
                                        valid_list.append("valid")
                                        break
                                elif room == connecting_rooms[-1]:
                                        #print("DEBUG: Invalid")
                                        invalid_path = True

                        if invalid_path == True:
                                print("Your arrow path was not valid, so your arrow entered a random neighbouring room")
                                break

                        x1 += 1
                        x2 += 1
                        
                #print(valid_list)

                if len(valid_list) == len(arrow_path) - 1:
                        #print("DEBUG: Arrow path is valid")
                        arrow_path = arrow_path[1:]
                        #print(f"DEBUG: Arrow path is {arrow_path}")
                else:
                        #print("DEBUG: Arrow path is invalid")
                        arrow_path = [random.choice(self.cave[self.player_location])]
                        #print(f"DEBUG: Arrow path is {arrow_path}")
                
                self.arrows -= 1

                if self.arrows < 1:
                        print("You have used your last arrow!")
                for room in arrow_path:

                        if room == self.threats["wump"]:
                                print("\033[1mYou Won: You sucessfully killed the wumpus!\033[0m")
                                self.wump_dead = True
                                break

                        elif room == self.player_location:
                                print("\033[1mGame Over: You shot yourself with your own arrow!\033[0m")
                                self.game_over = True
                                break
                        
                        elif room == arrow_path[-1]:
                                print("Your crooked arrow just hit a wall")
                                wump_chance = random.randint(1, 100)

                                if self.arrows == 0:
                                        print("\033[1mGame over: You ran out of arrows!\033[0m")
                                        self.game_over = True

                                elif wump_chance <= 25:
                                        Game.set_wump_room(self)
                                        #print("DEBUG: The wumpus moved because of the arrow")
                                        #print(f"DEBUG: The wumpus room is now {self.threats['wump']}")
                        
        
        def threat_warning(self):

                connecting_rooms = self.cave[self.player_location]

                if self.threats["wump"] in connecting_rooms:
                        print("\033[1mI can smell a wumpus nearby \033[0m")
                
                if self.threats["bat1"] in connecting_rooms or self.threats["bat2"] in connecting_rooms:
                        print("\033[1mI can hear bats nearby \033[0m")
                
                if self.threats["pit1"] in connecting_rooms or self.threats["pit2"] in connecting_rooms:
                        print("\033[1mI can feel a draft nearby \033[0m")
        
        def game_loop(self):
                replay = True
                print("Hunt The Wumpus")

                while replay:

                        self.arrows = 5
                        self.game_over = False
                        self.wump_dead = False
                        self.threats = {}
                        self.player_location = -1

                        Game.set_bat_rooms(self)
                        Game.set_pit_rooms(self)
                        Game.set_wump_room(self)
                        Game.set_player_spawn(self)
                        
                        #print(f"DEBUG: Locations of threats in the cave {self.threats}")
                        acceptable_actions = ["M", "MOVE", "S", "SHOOT", "Q", "QUIT", "H", "HELP"]

                        while not self.game_over and not self.wump_dead:

                                print("\n")
                                Game.threat_warning(self)
                                print(f"You are in room {self.player_location} and have {self.arrows} crooked arrows left") 
                                print(f"The connecting tunnels lead to rooms {self.cave[wump.player_location][0]}, {self.cave[wump.player_location][1]} and {self.cave[wump.player_location][2]}.")
                                action = input("Do you want to move(M), shoot(S), quit(Q), or need help(H)?: ")
                                action = action.upper()
                
                                if action in acceptable_actions[0:2]:
                                        Game.move_action(self)
                                
                                elif action in acceptable_actions[2:4]:
                                        Game.shoot_action(self)
                                
                                elif action in acceptable_actions[4:6]:
                                        print("\nThere is still a wumpus that needs to be killed!")
                                        exit_choice = input("Are you sure you want to quit? Press Y and press enter to exit: ")
                                        exit_choice = exit_choice.upper()

                                        if exit_choice == "Y" or exit_choice == "YES":
                                                sys.exit()
                                
                                elif action in acceptable_actions[6:]:
                                        Game.help()
                                
                                else:
                                        print("Sorry, I do not understand")
                        
                        while True:
                                new_game = input("\nDo you want to play a new game? (Y, N): ")
                                new_game = new_game.upper()

                                if new_game == "Y" or new_game == "YES":
                                        replay = True
                                        break

                                elif new_game == "N" or new_game == "NO":
                                        replay = False
                                        break

                                else:
                                        print("Sorry, I do not understand")








                
if __name__ == "__main__":
        wump = Game()
        wump.game_loop()
