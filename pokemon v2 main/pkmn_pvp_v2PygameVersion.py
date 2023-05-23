import pygame
from pygame.locals import *
import numpy as np
import pandas as pd
import random 
import sys 
from copy import deepcopy
import time
import os
from pygame import mixer

pygame.init()
mixer.init()

#Load Dataframes
pkmn_stats = pd.read_csv('pokemon v2 main/csv/pokemon_stats.csv') #Dataframe of all (10 included) Pokemon with HP,Attack,Defense,Type and Moves.
pkmn_stats.loc['Choose Pokemon','Name']='Choose Pokemon'

type_matchups = pd.read_csv('pokemon v2 main/csv/type_matchups.csv').T #Stores all 12 types(included), with their weaknesses,resistances and immunities. 
type_matchups.columns = ["weaknesses","resistances","immunities"] #assigns columns after transposing it

moves_df=pd.read_csv('pokemon v2 main/csv/moves.csv') #stores moves with type, damage, and other parameters
moves_df.index=moves_df.loc[:,'Name'] 

status_moves_df=pd.read_csv('pokemon v2 main/csv/status_moves.csv')
status_moves_df.index=status_moves_df.loc[:,'Name']


#Display
WIDTH,HEIGHT = 1000,700
DISPLAY_SIZE = (WIDTH,HEIGHT)
DISPLAY = pygame.display.set_mode(DISPLAY_SIZE)
pygame.display.set_caption("POKEMON GAME")

#Fonts
font30 = pygame.font.Font("pokemon v2 main/fonts/Pixeltype.ttf",30)
font40 = pygame.font.Font("pokemon v2 main/fonts/Pixeltype.ttf",40)
font60 = pygame.font.Font("pokemon v2 main/fonts/Pixeltype.ttf",60)
font80 = pygame.font.Font("pokemon v2 main/fonts/Pixeltype.ttf",80)
font100 = pygame.font.Font("pokemon v2 main/fonts/Pixeltype.ttf",100)

#Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (134,134,134)

#FPS
FPS = 60  
CLOCK = pygame.time.Clock()

#START SCREEN
ashpikachu = pygame.image.load("pokemon v2 main/assets/ashpikachu.png").convert_alpha()
ashpikachu = pygame.transform.scale(ashpikachu, (400, 500))
pkmn_background = pygame.image.load("pokemon v2 main/assets/startscreen.png").convert_alpha() #Pixel Art of a Gengar for the Start Screen, Spooky... 
pkmn_background = pygame.transform.scale(pkmn_background, DISPLAY_SIZE)
pkmn_logo = pygame.image.load("pokemon v2 main/assets/Pkmn_logo.png").convert_alpha() #Transparent, Black Pokemon Logo
pkmn_logo = pygame.transform.scale(pkmn_logo, (600,600))
blue_sky=pygame.image.load("pokemon v2 main/assets/blue_sky.jpg").convert() #Blue Sky for the PKMN selection screen.
blue_sky=pygame.transform.scale(blue_sky, DISPLAY_SIZE) 
TEXTBOX_image = pygame.image.load('pokemon v2 main/assets/textbox.png').convert_alpha()
TEXTBOX_image = pygame.transform.scale(TEXTBOX_image, (1000, 150))


#BATTLE SCREEN
battle_back = pygame.image.load('pokemon v2 main/assets/background.png')
battle_back = pygame.transform.scale(battle_back,(DISPLAY_SIZE))

#EVENTS
START_SCREEN = pygame.USEREVENT + 1
CHOOSE_PKMN = pygame.USEREVENT + 2
INIT_BATTLE = pygame.USEREVENT + 3
UPDATE_BATTLE_SCREEN = pygame.USEREVENT + 4
PICK_MOVE = pygame.USEREVENT + 5
UPDATE_HP = pygame.USEREVENT + 6
SHOW_TEXTBOX_OUTPUT = pygame.USEREVENT + 7
CHECK_WINNER = pygame.USEREVENT + 8
END_SCREEN = pygame.USEREVENT + 9

button_sound = pygame.mixer.Sound('pokemon v2 main/Music/button sound.mp3')

def draw_start_screen():  
    mixer.music.play(-1)  
    StartText=font60.render('PRESS SPACE TO START',0,'Black')
    text = font60.render("CUSTOM                EDITION", 0, BLACK)
    DISPLAY.blit(pkmn_background, (0, 0))
    
    pygame.display.update()
    pygame.time.delay(750)
    DISPLAY.blit(pkmn_logo,(200, -220)) #WIDTH * 25/800 = 25 when WIDTH=800
    pygame.display.update()
    pygame.time.delay(750)
    DISPLAY.blit(ashpikachu, (260, 140))
    pygame.display.update()
    pygame.time.delay(750)
    DISPLAY.blit(text, (300, 340))
    pygame.display.update()
    pygame.time.delay(750)
    DISPLAY.blit(StartText,(WIDTH//2-StartText.get_width()//2,HEIGHT-50))



def pkmn_selection_screen(player1choice,player2choice):
    toptext=font100.render("CHOOSE YOUR POKEMON!",0,'YELLOW')
    toptextrect=toptext.get_rect(center=(WIDTH//2,50))

    starttext = font100.render("PRESS ENTER TO START YOUR BATTLE!!", 0, "GREEN")
    starttext = pygame.transform.scale(starttext, (600, 40))


    player1text=font60.render(f"Player1:{pkmn_stats.loc[player1choice,'Name']}",0,'White') #render() has 3 required arguments:
    player2text=font60.render(f"Player2:{pkmn_stats.loc[player2choice,'Name']}",0,'White') #1.Text to render
                                                                                            #2.Whether to Anti-Alias
                                                                                            #3.Color of text
    randomtext=font60.render('Pick Random',0,'Dark Blue')
    randomrect = randomtext.get_rect(topleft = (600,125))

    DISPLAY.blit(blue_sky,(0,0))
    DISPLAY.blit(toptext,toptextrect)
    DISPLAY.blit(player1text,(10,100))
    DISPLAY.blit(player2text,(10,150))
    DISPLAY.blit(starttext, (200, 220))
    pygame.draw.rect(DISPLAY, "Yellow", (randomrect.x -8, randomrect.y -8, randomrect.width +8 , randomrect.height +8), border_radius=5)
    DISPLAY.blit(randomtext, randomrect)
    pygame.draw.rect(DISPLAY, "Dark Blue", (randomrect.x -8, randomrect.y -8, randomrect.width +8 , randomrect.height +8), width=2, border_radius=5)
    
    
    potrait_rect_list=[]
    for i in range(1,6):
        pokemon_potrait = pygame.image.load(f'pokemon v2 main/assets/potraits/{i}.png').convert_alpha()
        pokemon_potrait = pygame.transform.scale(pokemon_potrait,(120,120))
        potrait_rect=pokemon_potrait.get_rect(center=(WIDTH*i/5-WIDTH/10,350))
        potrait_rect_list.append(potrait_rect)
        DISPLAY.blit(pokemon_potrait,potrait_rect)

    potrait_rect_list2=[]
    for i in range(6,11):
        pokemon_potrait = pygame.image.load(f'pokemon v2 main/assets/potraits/{i}.png').convert_alpha()
        pokemon_potrait = pygame.transform.scale(pokemon_potrait,(120,120))
        potrait_rect=pokemon_potrait.get_rect(center=(WIDTH*(i-5)/5-WIDTH/10,550))
        potrait_rect_list2.append(potrait_rect)
        DISPLAY.blit(pokemon_potrait,potrait_rect)

    potrait_rect_list.extend(potrait_rect_list2)
    
    if player1choice != 'Choose Pokemon':
        if player1choice == 0:
            player1potrait = pygame.image.load(f"pokemon v2 main/assets/potraits/10.png").convert_alpha()
        else:
            player1potrait = pygame.image.load(f"pokemon v2 main/assets/potraits/{player1choice}.png").convert_alpha()
        DISPLAY.blit(player1potrait,(360,90))
    if player2choice != 'Choose Pokemon':
        if player2choice == 0:
            player2potrait = pygame.image.load(f"pokemon v2 main/assets/potraits/10.png").convert_alpha()
        else:
            player2potrait = pygame.image.load(f"pokemon v2 main/assets/potraits/{player2choice}.png").convert_alpha()
        DISPLAY.blit(player2potrait,(360,140))

    pygame.display.update()
    return potrait_rect_list, randomrect
    
    
def take_user_input(event,player1choice,player2choice):
    if event.key == K_1:
        player1choice,player2choice = set_player_choice(1,player1choice,player2choice)
        button_sound.play()
    if event.key == K_2:
        player1choice,player2choice = set_player_choice(2,player1choice,player2choice)
        button_sound.play()
    if event.key == K_3:
        player1choice,player2choice = set_player_choice(3,player1choice,player2choice)
        button_sound.play()
    if event.key == K_4:
        player1choice,player2choice = set_player_choice(4,player1choice,player2choice)
        button_sound.play()
    if event.key == K_5:
        player1choice,player2choice = set_player_choice(5,player1choice,player2choice)
        button_sound.play()
    if event.key == K_6:
        player1choice,player2choice = set_player_choice(6,player1choice,player2choice)
        button_sound.play()
    if event.key == K_7:
        player1choice,player2choice = set_player_choice(7,player1choice,player2choice)
        button_sound.play()
    if event.key == K_8:
        player1choice,player2choice = set_player_choice(8,player1choice,player2choice)
        button_sound.play()
    if event.key == K_9:
        player1choice,player2choice = set_player_choice(9,player1choice,player2choice)
        button_sound.play()
    if event.key == K_0:
        player1choice,player2choice = set_player_choice(0,player1choice,player2choice)
        button_sound.play()
    return player1choice,player2choice

def set_player_choice(choice,player1choice,player2choice):
    if player1choice == 'Choose Pokemon': 
        player1choice = choice
        pkmn_selection_screen(player1choice,player2choice)
    else:
        player2choice =  choice
        pkmn_selection_screen(player1choice,player2choice)
        
    return player1choice,player2choice
    
def initialize_player_pokemon(player1choice,player2choice):
    player1series=pkmn_stats.loc[player1choice,:]
    player2series=pkmn_stats.loc[player2choice,:]
    player1pokemon=Pokemon(*player1series['Name':'Type'],player1series['Move1':'Move4'],None)
    player2pokemon=Pokemon(*player2series['Name':'Type'],player2series['Move1':'Move4'],None)

    return player1pokemon,player2pokemon

def initialize_moves(player1pokemon,player2pokemon):
    player1moves=[]
    for move in player1pokemon.moves:
        move = Move(*moves_df.loc[move,'Name':'Turn_no'],moves_df.loc[move,'Status Effect':'Status Chance'],*moves_df.loc[move,'Accuracy':'Recoil'])
        if move.type_ == 'Status':
            move = StatusMove(*status_moves_df.loc[move.name,:],moves_df.loc[move.name,'Accuracy'])
        player1moves.append(move)
    player1pokemon.moves=player1moves
    
    player2moves=[]
    for move in player2pokemon.moves:
        move=Move(*moves_df.loc[move,'Name':'Turn_no'],moves_df.loc[move,'Status Effect':'Status Chance'],*moves_df.loc[move,'Accuracy':'Recoil'])
        if move.type_ == 'Status':
            move = StatusMove(*status_moves_df.loc[move.name,:],moves_df.loc[move.name,'Accuracy'])
        player2moves.append(move)
    player2pokemon.moves=player2moves
    
    return player1pokemon,player2pokemon

def initialize_sprites(player1pokemon,player2pokemon):
    player1pokemon.front_sprite = pygame.image.load(f'pokemon v2 main/assets/Pkmn_front/{player1pokemon.name}.png').convert_alpha()
    player1pokemon.back_sprite = pygame.image.load(f'pokemon v2 main/assets/Pkmn_back/{player1pokemon.name}_b.png').convert_alpha()

    player2pokemon.front_sprite = pygame.image.load(f'pokemon v2 main/assets/Pkmn_front/{player2pokemon.name}.png').convert_alpha()
    player2pokemon.back_sprite = pygame.image.load(f'pokemon v2 main/assets/Pkmn_back/{player2pokemon.name}_b.png').convert_alpha()

    return player1pokemon,player2pokemon


def turn_handler(player1pokemon,player2pokemon,turn=1):
    if turn == 1: 
        currentpokemon = player1pokemon
        opposingpokemon = player2pokemon
    elif turn == 2:
        currentpokemon = player2pokemon
        opposingpokemon = player1pokemon
    return currentpokemon, opposingpokemon, turn

def draw_battle_screen(currentpokemon, opposingpokemon,turn_damage=0):
    DISPLAY.blit(battle_back, (0, 0))
    draw_pokemon(currentpokemon, opposingpokemon)
    draw_hp_and_text_boxes(currentpokemon, opposingpokemon)
    update_HP(currentpokemon,opposingpokemon)
    

def draw_pokemon(currentpokemon,opposingpokemon):

    currentpokemon.back_sprite = pygame.transform.scale(currentpokemon.back_sprite, (400,400))
    opposingpokemon.front_sprite = pygame.transform.scale(opposingpokemon.front_sprite, (300,300))

    DISPLAY.blit(currentpokemon.back_sprite, (70, 230)) #actual pokemon sprites
    DISPLAY.blit(opposingpokemon.front_sprite, (530,130))
    
def draw_hp_and_text_boxes(currentpokemon,opposingpokemon):

    Pkmn1HpBoxName = font40.render(currentpokemon.name, 0, "BLACK")
    Pkmn2HpBoxName = font40.render(opposingpokemon.name, 0, "BLACK")

    HPTEXT= font60.render("HP:", 0, "BLACK")
    HPTEXT = pygame.transform.scale(HPTEXT, (40, 20))

    hpboxP1 = pygame.image.load('pokemon v2 main/assets/HPbox1.png').convert_alpha()
    hpboxP1 = pygame.transform.scale(hpboxP1, (450, 160))
    
    hpboxP2 = pygame.image.load('pokemon v2 main/assets/HPbox1.png').convert_alpha()
    hpboxP2 = pygame.transform.flip(hpboxP2, True, False)
    hpboxP2 = pygame.transform.scale(hpboxP2, (450, 160))

    DISPLAY.blit(hpboxP1, (540, 400)) #the actual box
    DISPLAY.blit(hpboxP2, (20, 40))

    DISPLAY.blit(HPTEXT, (610, 480)) #text saying HP: inside the box
    DISPLAY.blit(HPTEXT, (90, 120))

    DISPLAY.blit(Pkmn2HpBoxName, (90, 80)) #name of pokemon inside the box
    DISPLAY.blit(Pkmn1HpBoxName, (610, 440))
    DISPLAY.blit(TEXTBOX_image,(0,550))

    statusdict={'Burn':['BRN',RED],'Paralyze':['PAR',YELLOW],'Sleep':['SLP',GRAY],'Freeze':['FRZ','Blue'], 'Immobilise':['ATR', GREEN]}
    if currentpokemon.status:
        status_text = statusdict[currentpokemon.status][0]
        status_color=statusdict[currentpokemon.status][1]
        status_text = font30.render(status_text,0,status_color)
        DISPLAY.blit(status_text,(750, 444))
        pygame.draw.rect(DISPLAY,status_color,(750-2, 444-2,status_text.get_width()+3,status_text.get_height()+3),width=1,border_radius=5)
    
    if opposingpokemon.status:
        status_text = statusdict[opposingpokemon.status][0]
        status_color=statusdict[opposingpokemon.status][1]
        status_text = font30.render(status_text,0,status_color)
        DISPLAY.blit(status_text,(230, 84))
        pygame.draw.rect(DISPLAY,status_color,(230-2, 84-2,status_text.get_width()+3,status_text.get_height()+3),width=1,border_radius=5)

    pygame.display.update()

def update_HP(currentpokemon, opposingpokemon, turn_damage = 0):

    maxHP1 = currentpokemon.maxHP
    maxHP2 = opposingpokemon.maxHP
    
    maxHPtext1 = font30.render(f"{str(currentpokemon.currentHP)}/{str(currentpokemon.maxHP)}", 0, "BLACK")
    maxHPtext2 = font30.render(f"{str(opposingpokemon.currentHP)}/{str(opposingpokemon.maxHP)}", 0, "BLACK")

    pygame.draw.rect(DISPLAY,BLACK,(659,479,252,17)) #HP BAR BORDER
    pygame.draw.rect(DISPLAY, RED, (660, 480, 250, 15)) #RED IS UNDER THE GREEN 
    pygame.draw.rect(DISPLAY, GREEN, (660, 480, currentpokemon.currentHP/maxHP1 * 250, 15)) # GREEN IS OVERLAPPING RED AND AS 
    DISPLAY.blit(maxHPtext1, (840, 500))                                                    # THE POKEMON TAKES DAMAGE THE GREEN 
                                                                                            # WILL BE REDUCED RED WILL BE AS IT IS

    opposingpokemon.currentHP -= turn_damage
    
    pygame.draw.rect(DISPLAY,BLACK,(139,119,252,17)) #HP BAR BORDER
    pygame.draw.rect(DISPLAY, RED, (140, 120, 250, 15)) #RED IS UNDER THE GREEN 
    pygame.draw.rect(DISPLAY, GREEN, (140, 120, opposingpokemon.currentHP/maxHP2 * 250, 15)) # GREEN IS OVERLAPPING RED AND AS 
    DISPLAY.blit(maxHPtext2, (320, 140))                                                     # THE POKEMON TAKES DAMAGE THE GREEN WILL REDUCE
    pygame.display.update()    
    pygame.display.update()

def End_Screen(currentpokemon, opposingpokemon):
    mixer.music.load("pokemon v2 main/Music/End_Game.mp3")
    mixer.music.set_volume(1)
    mixer.music.play()
    End_img = pygame.image.load("pokemon v2 main/assets/textbox.png").convert_alpha()
    End_img = pygame.transform.scale(End_img, (950, 550))

    result = font60.render("BATTLE RESULT!", 0, BLACK)

    restart = font60.render("PRESS R TO PLAY AGAIN!", 0, 'Blue')

    DISPLAY.blit(End_img, (30, 15))
    DISPLAY.blit(result, (360, 100))

    DISPLAY.blit(restart, (300, 450))
    DISPLAY.blit(result, (360, 100))
    pygame.draw.rect(DISPLAY, "Blue", (300-8, 450-8,restart.get_width()+8,restart.get_height()+2),width=2,border_radius=5)
    
    if currentpokemon.currentHP <=0:
        loser = currentpokemon.name
        winner = opposingpokemon.name

    elif opposingpokemon.currentHP <=0:
        loser = opposingpokemon.name
        winner = currentpokemon.name

    winner_img = pygame.image.load(f"pokemon v2 main/assets/Pkmn_front/{winner}.png")    
    winner_img = pygame.transform.scale(winner_img, (250, 250))
    loser_img = pygame.image.load(f"pokemon v2 main/assets/Pkmn_front/{loser}.png")    
    loser_img = pygame.transform.scale(loser_img, (250, 250))
    winner_surf = font60.render(winner + " WON", 0, WHITE)
    loser_surf = font60.render(loser + " LOST", 0, WHITE)
    
    pygame.draw.rect(DISPLAY,GREEN,(142-2, 185-2,winner_img.get_width()+60,winner_img.get_height()+3),width=5,border_radius=5)
    pygame.draw.rect(DISPLAY,RED,(582-2, 185-2,loser_img.get_width()+60,loser_img.get_height()+3),width=5,border_radius=5)
    pygame.draw.rect(DISPLAY, RED, (580, 140, 310, 80))
    pygame.draw.rect(DISPLAY, GREEN, (140, 140, 310, 80))
    
    DISPLAY.blit(loser_surf, (600, 160))
    DISPLAY.blit(winner_surf, (150, 160))
    DISPLAY.blit(winner_img, (180, 200))   
    DISPLAY.blit(loser_img, (620, 200)) 

    pygame.display.update()
                                                
def show_moves(currentpokemon):

    move_text_positions=((50,580),(325,580),(50,635),(325,635))
    
    move_text_rect_list=[]
    for move, position in zip(currentpokemon.moves, move_text_positions):
        move_text=font60.render(move.name,0,'Black')
        move_text_rect = move_text.get_rect(topleft=position)
        DISPLAY.blit(move_text,move_text_rect)
        move_text_rect_list.append(move_text_rect)
    trainertext=font40.render(f'{currentpokemon.name}\'s Trainer,',0,'Black')
    pickyourmovetext=font40.render('Pick your Move!',0,'Black')


    DISPLAY.blit(trainertext,(600,580))
    DISPLAY.blit(pickyourmovetext,(600,625))
    return move_text_rect_list

def apply_status_effects(opposingpokemon, textbox_lines):
    if opposingpokemon.status is None:
        return opposingpokemon,textbox_lines
    elif opposingpokemon.status == 'Burn':
        opposingpokemon.currentHP -= opposingpokemon.currentHP/10
        textbox_lines.append(f'{opposingpokemon.name} was hurt by its Burn.')

    return opposingpokemon,textbox_lines

def turn_swapper(turn):
    if turn == 1: return 2
    elif turn == 2: return 1

def clear_textbox():
    DISPLAY.blit(TEXTBOX_image, (0, 550)) #text box at the bottom
    pygame.display.update()

def textbox_output(textbox_lines):
    if len(textbox_lines) == 1:
        line1 = font60.render(textbox_lines[0],0,'Black')
        DISPLAY.blit(line1,(50,580))
        pygame.display.update()
        pygame.time.delay(500)

    else:
        for lineindex in range(len(textbox_lines)-1):
            line1 = font60.render(textbox_lines[lineindex],0,'Black')
            DISPLAY.blit(line1,(50,580))
            pygame.display.update()
            pygame.time.delay(500)
            line2 = font60.render(textbox_lines[lineindex+1],0,'Black')
            DISPLAY.blit(line2,(50,635))
            pygame.display.update()
            pygame.time.delay(500)
            clear_textbox()

def apply_stat_modifiers(currentpokemon,opposingpokemon):
    if currentpokemon.attack_modifier >= 0:
        attack = currentpokemon.attack * (1 + currentpokemon.attack_modifier/4)
    if opposingpokemon.defense_modifier >= 0:
        defense = opposingpokemon.defense * (1 + opposingpokemon.defense_modifier/4)
    return attack, defense

def check_chance(chance):
    if random.random() <= chance:
        return True
    return False
    
def check_type_effectiveness(move_chosen,opposingpokemon,textbox_lines):
    if move_chosen.type_ in type_matchups.loc[opposingpokemon.type_,'weaknesses'].split(','):
        type_multiplier = 2
        textbox_lines.append("It was Super Effective!")
    elif move_chosen.type_ in type_matchups.loc[opposingpokemon.type_,'resistances'].split(','):
        type_multiplier = 0.5
        textbox_lines.append("It was not very Effective...")
    elif move_chosen.type_ in type_matchups.loc[opposingpokemon.type_,'immunities'].split(','):
        type_multiplier = 0
        textbox_lines.append(f"{opposingpokemon.name} is immune to this attack.")
    else: 
        type_multiplier = 1
    return type_multiplier,textbox_lines

def check_stab(currentpokemon,move_chosen):
    if move_chosen.type_ == currentpokemon.type_:
        return 1.5
    else: 
        return 1

class Pokemon:
    def __init__(self,name,maxHP,attack,defense,type_,moves,status=None,currentHP=None):
        self.name=name
        self.maxHP=maxHP
        self.attack=attack
        self.defense=defense
        self.type_ = type_
        self.moves = moves
        self.status = status
        self.currentHP = maxHP
        self.front_sprite=None
        self.back_sprite=None
        self.is_charging = 0
        self.attack_modifier = 0 
        self.defense_modifier = 0 

    # def do_attack_animation(self,opposingpokemon):
    #    DISPLAY.blit(battle_back, (0, 0))
    #    draw_hp_and_text_boxes(self,opposingpokemon)
    #    update_HP(self,opposingpokemon)
    #    self.back_sprite = pygame.transform.scale(self.back_sprite, (400,400))
    #    opposingpokemon.front_sprite = pygame.transform.scale(opposingpokemon.front_sprite, (300,300))

    #    DISPLAY.blit(self.back_sprite, (70, 230))
    #    DISPLAY.blit(opposingpokemon.front_sprite, (530,130))
    #    pygame.display.update()
    #    DISPLAY.blit(opposingpokemon.front_sprite, (540,130))
    #    pygame.display.update()

    def perform_attack(self, move_chosen_no, opposingpokemon, turn):
        
        # self.do_attack_animation(opposingpokemon)
        textbox_lines = []
        move_chosen = self.moves[move_chosen_no]
        
        do_turn, textbox_lines = self.check_move_inhibiting_status(textbox_lines)

        if do_turn:
            textbox_lines.append(f"{self.name} used {move_chosen.name} !" )


            if check_chance(move_chosen.accuracy):
                if move_chosen.type_ != 'Status':
                    if move_chosen.turn_count == move_chosen.turn_no:
                        move_chosen.turn_count = 1
                        self.is_charging = 0

                        attack,defense = apply_stat_modifiers(self,opposingpokemon)

                        type_multiplier, textbox_lines = check_type_effectiveness(move_chosen,opposingpokemon,textbox_lines)
                        stab = check_stab(self,move_chosen)
                        if check_chance(0.0625):
                            crit = 1.5
                            textbox_lines.append('A Critical Hit!')
                        else: crit = 1

                        turn_damage = int((attack/defense * move_chosen.damage//10) * type_multiplier * stab * crit)

                        status_effect = move_chosen.effects[0] 
                        status_chance = move_chosen.effects[1]
                        if status_chance:
                            if check_chance(status_chance) and opposingpokemon.status is None:
                                opposingpokemon.status = status_effect
                                textbox_lines.append(f'{opposingpokemon.name} was inflicted with {status_effect}')
                                if opposingpokemon.status == 'Burn': opposingpokemon.attack *= 0.75
                        
                        if move_chosen.recoil:
                            self.currentHP -= int(move_chosen.recoil * turn_damage)
                            textbox_lines.append(f"{self.name} was hurt in recoil")
                        print(f'{self.name} did {turn_damage} damage')
                    
                    else:
                            turn_damage = 0
                            textbox_lines.append(f'{self.name} is charging for its attack.')
                            move_chosen.turn_count += 1
                            self.is_charging = move_chosen_no
                    
                elif move_chosen.type_ == 'Status':
                    textbox_lines = self.perform_status_move(move_chosen,opposingpokemon,textbox_lines)  
                    turn_damage = 0
            else: 
                textbox_lines.append(f'{self.name} missed.')
                turn_damage = 0   
        else: turn_damage = 0

        if opposingpokemon.status == 'Burn':
            opposingpokemon.currentHP -= int(opposingpokemon.maxHP * 0.1)
            textbox_lines.append(f'{opposingpokemon.name} was hurt by its Burn.')

        return turn_damage ,textbox_lines

    def perform_status_move(self,move_chosen,opposingpokemon,textbox_lines):
        if move_chosen.category == 'SelfBoost':
                if move_chosen.effect == 'Attack':
                    if self.attack_modifier < 6:
                        self.attack_modifier += 2
                        textbox_lines.append(f"{self.name}'s Attack Sharply Rose!")
                    else:
                        textbox_lines.append(f"{self.name}'s Attack cannot go any higher!")
                if move_chosen.effect == 'Defense':
                    if self.defense_modifier < 6:
                        self.defense_modifier += 2
                        textbox_lines.append(f"{self.name}'s Defense Sharply Rose!")
                    else:
                        textbox_lines.append(f"{self.name}'s Defense cannot go any higher!")
                
                if move_chosen.effect == 'Attack,Defense':
                    if self.attack_modifier < 6:
                        self.attack_modifier += 1
                        textbox_lines.append(f"{self.name}'s Attack Rose!")
                    else:
                        textbox_lines.append(f"{self.name}'s Attack cannot go any higher!")
                    if self.defense_modifier < 6:
                        self.defense_modifier += 1
                        textbox_lines.append(f"{self.name}'s Defense Rose!")
                    else:
                        textbox_lines.append(f"{self.name}'s Defense cannot go any higher!")

                
                if move_chosen.effect == 'Heal':
                    self.currentHP += self.maxHP * 0.4
                    if self.currentHP >= self.maxHP: self.currentHP = self.maxHP
                    textbox_lines.append(f"{self.name}'s gained some Health")

        if move_chosen.category == 'StatusEffect':
            if opposingpokemon.status is None:
                if move_chosen.effect == 'Paralyze':
                    opposingpokemon.status = 'Paralyze'
                    textbox_lines.append(f'{opposingpokemon.name} was paralyzed.')
                if move_chosen.effect == 'Sleep':
                    opposingpokemon.status = 'Sleep'
                    textbox_lines.append(f'{opposingpokemon.name} fell asleep.')
                if move_chosen.effect == 'Immobilise':
                    opposingpokemon.status = 'Immobilise'
                    textbox_lines.append(f'{opposingpokemon.name} was immobilised by attraction.')
            else: 
                textbox_lines.append(f'{opposingpokemon.name} is already {opposingpokemon.status}.')
        
        return textbox_lines

    def check_move_inhibiting_status(self,textbox_lines):
        if self.status == 'Sleep':
            if check_chance(0.4):
                textbox_lines.append(f'{self.name} Woke up!')
                self.status = None
            else:
                textbox_lines.append(f'{self.name} is fast asleep.')
                return 0, textbox_lines
        
        if self.status == 'Paralyze':
            if check_chance(0.7):
                pass
            else:
                textbox_lines.append(f'{self.name} could not move due to paralysis.')
                return 0, textbox_lines
        
        if self.status == 'Immobilise':
            if check_chance(0.35):
                textbox_lines.append(f'{self.name} broke out of its attraction')
                self.status = None
            else:
                textbox_lines.append(f'{self.name} is immobilised by attraction.')
                return 0, textbox_lines
        
        if self.status == 'Freeze':
            if check_chance(0.4):
                textbox_lines.append(f'{self.name} was unfrozen')
                self.status = None
            else:
                textbox_lines.append(f'{self.name} is frozen.')
                return 0,textbox_lines

        return True, textbox_lines

class Move:
    def __init__(self,name,type_,damage,turn_no,effects,accuracy,recoil):
        self.name = name
        self.type_ = type_
        self.damage = damage
        self.effects = effects
        self.turn_no = turn_no
        self.accuracy = accuracy
        self.recoil = recoil
        self.turn_count = 1

class StatusMove:
    def __init__(self,name,type_,category,effect,accuracy):
        self.name = name
        self.type_ = type_
        self.category = category
        self.effect = effect
        self.accuracy = accuracy

def main():
    game_status = 'START_SCREEN'
    pygame.event.post(pygame.event.Event(START_SCREEN))
    player1choice='Choose Pokemon'
    player2choice='Choose Pokemon'
    turn=1
    turn_damage = 0
    while game_status != 'quit':
        for event in pygame.event.get():
            if event.type == QUIT:
                game_status = 'QUIT'
                pygame.quit()
                sys.exit()

            if event.type == START_SCREEN:
                mixer.music.load("pokemon v2 main/Music/Game.mp3")
                mixer.music.set_volume(0.7)
                mixer.music.play(-1)
                draw_start_screen()

            if event.type == CHOOSE_PKMN:
                game_status='CHOOSE_PKMN'
                potrait_rect_list, randomrect = pkmn_selection_screen(player1choice,player2choice)
            
            if event.type == INIT_BATTLE:
                game_status='INIT_BATTLE'

                player1pokemon,player2pokemon = initialize_player_pokemon(player1choice,player2choice)
                player1pokemon,player2pokemon = initialize_moves(player1pokemon,player2pokemon)
                player1pokemon,player2pokemon = initialize_sprites(player1pokemon,player2pokemon)
                currentpokemon, opposingpokemon, turn = turn_handler(player1pokemon,player2pokemon,turn)
                pygame.event.post(pygame.event.Event(UPDATE_BATTLE_SCREEN))
                mixer.music.load("pokemon v2 main/Music/Pkmn_Battle.mp3")
                mixer.music.set_volume(0.7)
                mixer.music.play(-1)

            if event.type == UPDATE_BATTLE_SCREEN:
                game_status = 'UPDATE_BATTLE_SCREEN'
                currentpokemon, opposingpokemon, turn = turn_handler(player1pokemon,player2pokemon,turn)
                draw_battle_screen(currentpokemon, opposingpokemon)
                pygame.event.post(pygame.event.Event(PICK_MOVE))

            if event.type == PICK_MOVE:
                game_status = 'PICK_MOVE'
                if not currentpokemon.is_charging:
                    move_text_rect_list = show_moves(currentpokemon)
                else:
                    turn_damage , textbox_lines = currentpokemon.perform_attack(currentpokemon.is_charging, opposingpokemon,turn)
                    pygame.event.post(pygame.event.Event(UPDATE_HP))

            if event.type == UPDATE_HP:
                game_status = 'UPDATE_HP'
                draw_pokemon(currentpokemon,opposingpokemon)
                draw_hp_and_text_boxes(currentpokemon,opposingpokemon)
                update_HP(currentpokemon, opposingpokemon, turn_damage)
                pygame.time.delay(1000)
                
                turn = turn_swapper(turn)
                currentpokemon, opposingpokemon, turn = turn_handler(player1pokemon,player2pokemon,turn)
                pygame.event.post(pygame.event.Event(SHOW_TEXTBOX_OUTPUT))

            if event.type == SHOW_TEXTBOX_OUTPUT:
                clear_textbox()
                textbox_output(textbox_lines)
                pygame.event.post(pygame.event.Event(CHECK_WINNER))

            if event.type == CHECK_WINNER:
                game_ended = False
                if currentpokemon.currentHP <= 0 or opposingpokemon.currentHP <=0:
                    End_Screen(currentpokemon, opposingpokemon)
                    game_ended = True
                if not game_ended:
                    pygame.event.post(pygame.event.Event(UPDATE_BATTLE_SCREEN))
            if event.type == KEYDOWN:
                if (event.key==K_SPACE) and game_status == 'START_SCREEN': #START GAME USING SPACE 
                    pygame.event.post(pygame.event.Event(CHOOSE_PKMN))
                    button_sound.play()
                
                if game_status == 'CHOOSE_PKMN':
                    player1choice,player2choice = take_user_input(event,player1choice,player2choice)
                    
                    if (event.key == K_RETURN) and player1choice != 'Choose Pokemon' and player2choice != 'Choose Pokemon':  #Pressing Enter the Battle will begin
                        pygame.event.post(pygame.event.Event(INIT_BATTLE))
                        button_sound.play()               

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if game_status == 'START_SCREEN': #START GAME USING MOUSE
                        pygame.event.post(pygame.event.Event(CHOOSE_PKMN))
                        button_sound.play()
                    
                    if game_status == 'CHOOSE_PKMN':  #SELECT POKEMON FROM SELECTION SCREEN USING MOUSE
                        i = 1
                        for potrait_rect in potrait_rect_list:
                            if potrait_rect.collidepoint(event.pos):
                                    player1choice,player2choice = set_player_choice(int(str(i)[-1]),player1choice,player2choice)    
                                    #the int(str(i[-1])) is to take last digit of every number since machamp is 10th        
                                    button_sound.play()                 
                            i+=1
                        if randomrect.collidepoint(event.pos):
                            player1choice,player2choice = set_player_choice(random.randint(0,9),player1choice,player2choice)
                            button_sound.play()
                    if game_status == 'PICK_MOVE':
                        move_chosen_no = 0
                        for move_text_rect in move_text_rect_list:
                            if move_text_rect.collidepoint(event.pos):

                                turn_damage , textbox_lines = currentpokemon.perform_attack(move_chosen_no, opposingpokemon,turn)
                                pygame.event.post(pygame.event.Event(UPDATE_HP))
                            move_chosen_no+=1
            
            if event.type == KEYDOWN:
                if event.key == K_r:
                    main()   
        
        pygame.display.update()
        CLOCK.tick(FPS)

if __name__=='__main__':
    main()
    

