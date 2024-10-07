from typing import List, Tuple
import random
from itertools import count
import pandas as pd

    
class Robot():
    def __init__(self, 
                 id:int,
                 name: str, 
                 health: int, 
                 attack_type: str,
                 defence_type: str):
        self.id = id,      
        self.name = name
        self.health = health
        self.attack_type = attack_type
        self.defense_type = defence_type
        self.alive = True
 
    def attack(self, attack_type, target):
        print(self.name + ' attack '+ target.name + ' using '+ str(attack_type))
        if attack_type == 'tackle':
            target.health -= 30 
        if attack_type == 'hammer arm':
            target.health -= 35
        if attack_type == 'high jump kick':
            target.health -= 40
        
    def defense(self, defence_type):
        print(self.name + ' defended using '+ str(defence_type))
        if defence_type == 'light screen':
            self.health += 5
        if defence_type == 'iron defense':
            self.health += 10
        if defence_type == 'protect':
            self.health += 15

    def setalive(self):
        if self.health <= 0:
            self.alive = False
        if self.health > 0:
            self.alive = True

class Battle():
    def __init__(self, robot_a,robot_b):
        self.robot_a = robot_a
        self.robot_b = robot_b
    
    def begin_battle(robot_a, robot_b):
        print('--------------------------------')
        print("Battle Begin!")
        print('--------------------------------')
        print(f'{robot_a.name} vs {robot_b.name}!')

    def updateStatus(robot_a,robot_b, df):
        df.loc[df['id']== robot_a.id,['alive']]= robot_a.alive
        df.loc[df['id']== robot_b.id,['alive']]= robot_b.alive
        print(robot_a.health)
        print(robot_b.health)
        if robot_a.alive == False:
            df.loc[df['id']== robot_a.id,['health']] = 0
        if robot_b.alive == False:
            df.loc[df['id']== robot_b.id,['health']] = 0

    def battle(robot_a, robot_b):
        # battle
        running = True
        while running:      
            attack_list = ['tackle', 'hammer arm', 'high jump kick']
            defence_list = ['light screen', 'iron defense', 'protect']
            # a attack b
            attack_type = random.choice(attack_list)
            robot_a.attack(attack_type,robot_b)

            # b defence
            defence_type = random.choice(defence_list)
            robot_b.defense(defence_type)
            print(robot_b.name +' has '+ str(robot_b.health) + ' health remaining')

            # b attack a
            attack_type = random.choice(attack_list)
            robot_b.attack(attack_type,robot_a)

            # a defence
            defence_type = random.choice(defence_list)
            robot_a.defense(defence_type)
            print(robot_a.name + ' has '+ str(robot_a.health) + ' health remaining')

            #check_winner
            robot_a.setalive()
            robot_b.setalive()
            if robot_a.alive == False:
                print(robot_b.name +' won the battle! ')
                print('Battle Complete!')
                running = False

            elif robot_b.alive == False:    
                print(robot_a.name +' won the battle! ')
                print('Battle Complete!')
                running = False

class Game():
    def add_robot():
        start = input('Do you wish to battle? (yes/no)')
        if start == 'yes':
            Game.start_game()
        elif start == 'no':
            exit()
    
    def robot_selected(robot_a, robot_b):
        print('=====================================')
        print(f'{robot_a.name} selected!')
        print(f'{robot_b.name} selected!')
    
    def robot_available(robot_a, robot_b):
        print('=====================================')
        print(f'Robots Available: ')
        print(f'-- RoboOne')
        print(f'-- RoboTwo')
        print(f'-- RoboThree')

    def start_game():
        #get robot with alive = true
        df_alive = df.where(df['alive'] == True)
        #pilih 2 robot random
        df_alive = df_alive[~df_alive['id'].isna()].sample(2) 

        robot_a = Robot(df_alive['id'].iloc[0],
                df_alive['nama'].iloc[0], 
                df_alive['health'].iloc[0],attack_type, defence_type)
        robot_b = Robot(df_alive['id'].iloc[1],
                        df_alive['nama'].iloc[1], 
                        df_alive['health'].iloc[1],attack_type, defence_type)

        #begin batte
        Game.robot_available(robot_a,robot_b)
        Game.robot_selected(robot_a, robot_b)
        Battle.begin_battle(robot_a, robot_b)
        Battle.battle(robot_a,robot_b)

        #update HP dan status
        Battle.updateStatus(robot_a,robot_b,df)
        print(df)

# robot variables
attack_type = ''
defence_type = ''
initial_health = 100

# insert into robot attribute pandas table
# untuk menyimpan data robot 

df = pd.DataFrame({'id':[1,2,3],
                              'nama':['RoboOne','RoboTwo','RoboThree'],
                              'health':[initial_health, initial_health, initial_health],
                              'alive':[True,True,True]
                              })

runGame = True
Game.add_robot()