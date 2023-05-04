import pygame
from pygame.locals import *
import numpy as np
import pandas as pd
import random as rnd
import sys 
from copy import deepcopy

pygame.init()

#Load Dataframes
pkmn_stats = pd.read_csv('pokemon v2 main/csv/pokemon_stats.csv') #Dataframe of all (10 included) Pokemon with HP,Attack,Defense,Type and Moves.
pkmn_stats.loc['Choose Pokemon','Name']='Choose Pokemon'
type_matchups = pd.read_csv('pokemon v2 main/csv/type_matchups.csv').T #Stores all 12 types(included), with their weaknesses,resistances and immunities. 
type_matchups.columns = ["weaknesses","resistances","immunities"] #assigns columns after transposing it
moves_df=pd.read_csv('pokemon v2 main/csv/moves.csv') #stores moves with type, damage, and other parameters
moves_df.index=moves_df.loc[:,'Name'] 

#Display
WIDTH,HEIGHT = 1000,700
DISPLAY_SIZE = (WIDTH,HEIGHT)
DISPLAY = pygame.display.set_mode(DISPLAY_SIZE)
pygame.display.set_caption("POKEMON GAME")

#Fonts
font40 = pygame.font.Font("pokemon v2 main/fonts/Pixeltype.ttf",40)
font60 = pygame.font.Font("pokemon v2 main/fonts/Pixeltype.ttf",60)
font100 = pygame.font.Font("pokemon v2 main/fonts/Pixeltype.ttf",100)

#Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

#FPS
FPS = 60
CLOCK = pygame.time.Clock()

#START SCREEN
pkmn_background = pygame.image.load("pokemon v2 main/assets/gengar_pixels.jpeg").convert_alpha() #Pixel Art of a Gengar for the Start Screen, Spooky... 
pkmn_background = pygame.transform.scale(pkmn_background, DISPLAY_SIZE)
pkmn_logo = pygame.image.load("pokemon v2 main/assets/pkmn_logo.png").convert_alpha() #Transparent, Black Pokemon Logo
#pkmn_logo = pygame.transform.scale(pkmn_logo, (100,100))
blue_sky=pygame.image.load("pokemon v2 main/assets/blue_sky.jpg").convert() #Blue Sky for the PKMN selection screen.
blue_sky=pygame.transform.scale(blue_sky, DISPLAY_SIZE) 

#BATTLE SCREEN
battle_back = pygame.image.load('pokemon v2 main/assets/background.png')
battle_back = pygame.transform.scale(battle_back,(DISPLAY_SIZE))

#EVENTS
START_SCREEN = pygame.USEREVENT + 1
CHOOSE_PKMN = pygame.USEREVENT + 2
BATTLE = pygame.USEREVENT + 3

def draw_start_screen():    #Draw the start screen, includes Start text, pokemon logo, and Gengar background.
    StartText=font60.render('PRESS SPACE TO START',0,'Black')
    DISPLAY.blit(pkmn_background, (0, 0))
    DISPLAY.blit(pkmn_logo,(WIDTH//2-pkmn_logo.get_width()//2-WIDTH * 25/800, -30)) #WIDTH * 25/800 = 25 when WIDTH=800
    DISPLAY.blit(StartText,(WIDTH//2-StartText.get_width()//2,HEIGHT-60))
    pygame.display.update()

def pkmn_selection_screen(player1choice,player2choice):
    toptext=font100.render("CHOOSE YOUR POKEMON!",0,'YELLOW')
    toptextrect=toptext.get_rect(center=(WIDTH//2,50))

    starttext = font100.render("PRESS ENTER TO START YOUR BATTLE!!", 0, "GREEN")
    starttext = pygame.transform.scale(starttext, (600, 40))
    
    player1text=font60.render(f"Player1:{pkmn_stats.loc[player1choice,'Name']}",0,'White') #render() has 3 required arguments:
    player2text=font60.render(f"Player2:{pkmn_stats.loc[player2choice,'Name']}",0,'White') #1.Text to render
                                                                                            #2.Whether to Anti-Alias
                                                                                            #3.Color of text
    DISPLAY.blit(blue_sky,(0,0))
    DISPLAY.blit(toptext,toptextrect)
    DISPLAY.blit(player1text,(10,100))
    DISPLAY.blit(player2text,(10,150))
    DISPLAY.blit(starttext, (200, 200))
    
    potrait_rect_list=[]
    for i in range(1,6):
        pokemon_potrait = pygame.image.load(f'pokemon v2 main/assets/potraits/{i}.png').convert_alpha()
        pokemon_potrait = pygame.transform.scale(pokemon_potrait,(120,120))
        potrait_rect=pokemon_potrait.get_rect(center=(WIDTH*i/5-WIDTH/10,300))
        potrait_rect_list.append(potrait_rect)
        DISPLAY.blit(pokemon_potrait,potrait_rect)

    potrait_rect_list2=[]
    for i in range(6,11):
        pokemon_potrait = pygame.image.load(f'pokemon v2 main/assets/potraits/{i}.png').convert_alpha()
        pokemon_potrait = pygame.transform.scale(pokemon_potrait,(120,120))
        potrait_rect=pokemon_potrait.get_rect(center=(WIDTH*(i-5)/5-WIDTH/10,500))
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
    return potrait_rect_list
    
def take_user_input(event,player1choice,player2choice):
    if event.key == K_1:
        player1choice,player2choice = set_player_choice(1,player1choice,player2choice)
    if event.key == K_2:
        player1choice,player2choice = set_player_choice(2,player1choice,player2choice)
    if event.key == K_3:
        player1choice,player2choice = set_player_choice(3,player1choice,player2choice)
    if event.key == K_4:
        player1choice,player2choice = set_player_choice(4,player1choice,player2choice)
    if event.key == K_5:
        player1choice,player2choice = set_player_choice(5,player1choice,player2choice)
    if event.key == K_6:
        player1choice,player2choice = set_player_choice(6,player1choice,player2choice)
    if event.key == K_7:
        player1choice,player2choice = set_player_choice(7,player1choice,player2choice)
    if event.key == K_8:
        player1choice,player2choice = set_player_choice(8,player1choice,player2choice)
    if event.key == K_9:
        player1choice,player2choice = set_player_choice(9,player1choice,player2choice)
    if event.key == K_0:
        player1choice,player2choice = set_player_choice(0,player1choice,player2choice)
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
    player1pokemonbase=Pokemon(*player1series['Name':'Type'],player1series['Move1':'Move4'],None)
    player2pokemonbase=Pokemon(*player2series['Name':'Type'],player2series['Move1':'Move4'],None)
    player1pokemon = deepcopy(player1pokemonbase)
    player2pokemon = deepcopy(player2pokemonbase)

    return player1pokemon,player2pokemon,player1pokemonbase,player2pokemonbase

def initialize_moves(player1pokemon,player2pokemon):
    player1moves=[]
    for move in player1pokemon.moves:
        move=Move(*moves_df.loc[move,'Name':'Turn_no'],moves_df.loc[move,'Status Effect':'Status Chance'])
        player1moves.append(move)
    player1pokemon.moves=player1moves
    
    player2moves=[]
    for move in player2pokemon.moves:
        move=Move(*moves_df.loc[move,'Name':'Turn_no'],moves_df.loc[move,'Status Effect':'Status Chance'])
        player2moves.append(move)
    player2pokemon.moves=player2moves
    
    return player1pokemon,player2pokemon

def turn_handler(player1pokemon,player2pokemon,turn=1):
    if turn == 1: 
        currentpokemon = player1pokemon
        opposingpokemon = player2pokemon
    elif turn == 2:
        currentpokemon = player2pokemon
        opposingpokemon = player1pokemon
    return currentpokemon, opposingpokemon, turn

def load_sprites_text(currentpokemon,opposingpokemon):
    currentpokemon_name = currentpokemon.name
    opposingpokemon_name = opposingpokemon.name

    Pokemon1 = pygame.image.load(f'pokemon v2 main/assets/Pkmn_back/{currentpokemon_name}_b.png').convert_alpha()
    Pokemon2 = pygame.image.load(f'pokemon v2 main/assets/Pkmn_front/{opposingpokemon_name}.png').convert_alpha()
    Pokemon1 = pygame.transform.scale(Pokemon1, (400,400))
    Pokemon2 = pygame.transform.scale(Pokemon2, (300,300))

    textbox = pygame.image.load('pokemon v2 main/assets/textbox.png').convert_alpha()
    textbox = pygame.transform.scale(textbox, (1000, 150))

    Pkmn1HpBoxName = font40.render(currentpokemon_name, 0, "BLACK")

    Pkmn2HpBoxName = font40.render(opposingpokemon_name, 0, "BLACK")

    HPP1= font60.render("HP:", 0, "BLACK")
    HPP1 = pygame.transform.scale(HPP1, (40, 20))

    HPP2 = font60.render("HP:", 0, "BLACK")
    HPP2 = pygame.transform.scale(HPP2, (40, 20))

    hpboxP1 = pygame.image.load('pokemon v2 main/assets/HPbox1.png').convert_alpha()
    hpboxP1 = pygame.transform.scale(hpboxP1, (450, 160))
    
    hpboxP2 = pygame.image.load('pokemon v2 main/assets/HPbox1.png').convert_alpha()
    hpboxP2 = pygame.transform.flip(hpboxP2, True, False)
    hpboxP2 = pygame.transform.scale(hpboxP2, (450, 160))

    DISPLAY.blit(hpboxP1, (540, 400))
    DISPLAY.blit(hpboxP2, (20, 40))
    DISPLAY.blit(HPP1, (610, 480))
    DISPLAY.blit(HPP2, (90, 120))
    DISPLAY.blit(Pkmn2HpBoxName, (90, 80))
    DISPLAY.blit(Pkmn1HpBoxName, (610, 440))
    DISPLAY.blit(Pokemon1, (70, 230))
    DISPLAY.blit(Pokemon2, (530,130))
    DISPLAY.blit(textbox, (0, 550))
 

def HPpokemon1(currentpokemon, turn_damage = 0):
    maxHP1 = currentpokemon.HP
    NewHP1 = maxHP1 - turn_damage
    maxHPtext1 = font60.render(str(NewHP1), 0, "BLACK")
    maxHPtext1 = pygame.transform.scale(maxHPtext1, (40, 20))

    pygame.draw.rect(DISPLAY, RED, (660, 480, maxHP1, 15)) #RED IS UNDER THE GREEN 
    pygame.draw.rect(DISPLAY, GREEN, (660, 480, NewHP1, 15)) #GREEN IS OVERLAPPING RED AND AS THE POKEMON TAKES DAMAGE THE GREEN WILL BE REDUCED RED WILL BE AS IT IS

    DISPLAY.blit(maxHPtext1, (880, 500)) 


def HPpokemon2(opposingpokemon, turn_damage = 0):
    maxHP2 = opposingpokemon.HP
    NewHP2 = maxHP2 - turn_damage
    maxHPtext2 = font60.render(str(NewHP2), 0, "BLACK")
    maxHPtext2 = pygame.transform.scale(maxHPtext2, (40, 20))

    pygame.draw.rect(DISPLAY, RED, (140, 120, maxHP2, 15)) #RED IS UNDER THE GREEN 
    pygame.draw.rect(DISPLAY, GREEN, (140, 120, NewHP2, 15)) #GREEN IS OVERLAPPING RED AND AS THE POKEMON TAKES DAMAGE THE GREEN WILL BE REDUCED RED WILL BE AS IT IS

    DISPLAY.blit(maxHPtext2, (360, 140)) 

def draw_battle_screen(currentpokemon, opposingpokemon):
    DISPLAY.blit(battle_back, (0, 0))
    load_sprites_text(currentpokemon, opposingpokemon)
    HPpokemon1(currentpokemon, turn_damage = 0)
    HPpokemon2(opposingpokemon, turn_damage = 0)



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



class Pokemon:
    def __init__(self,name,HP,attack,defense,type_,moves,status=None):
        self.name=name
        self.HP=HP
        self.attack=attack
        self.defense=defense
        self.type_ = type_
        self.moves = moves
        self.status = status
    
    def perform_attack(self, move_chosen_no, opposingpokemon, turn):
        #print(f"{self.name} did {self.moves[move_chosen_no].name}")
        move_chosen = self.moves[move_chosen_no]
        # print(move_chosen.type_)
        # print(type_matchups.loc[opposingpokemon.type_,'weaknesses'].split())
        # print(self.attack)
        # print(opposingpokemon.defense)
        # print(move_chosen.damage)
        # print(move_chosen.type_ in type_matchups.loc[opposingpokemon.type_,'weaknesses'].split(','))
        if move_chosen.type_ != 'Status':
            if move_chosen.type_ in type_matchups.loc[opposingpokemon.type_,'weaknesses'].split(','):
                type_multiplier = 2
            elif move_chosen.type_ in type_matchups.loc[opposingpokemon.type_,'resistances'].split(','):
                type_multiplier = 0.5
            elif move_chosen.type_ in type_matchups.loc[opposingpokemon.type_,'immunities'].split(','):
                type_multiplier = 0
            else: type_multiplier = 1
        else:
            type_multiplier = 1
            move_chosen.damage = 80
        turn_damage = ((self.attack/opposingpokemon.defense) * move_chosen.damage * type_multiplier)//4
        print(f'{self.name} did {turn_damage} damage')
        
        if turn == 1:
            turn = 2
        elif turn == 2:
            turn = 1
        return turn_damage,turn

            
        


class Move:
    def __init__(self,name,type_,damage,turn_no,effects):
        self.name=name
        self.type_ = type_
        self.damage = damage
        self.effects = effects
        self.turn_no=turn_no
    
def main():
    game_status = 'START_SCREEN'
    pygame.event.post(pygame.event.Event(START_SCREEN))
    player1choice='Choose Pokemon'
    player2choice='Choose Pokemon'
    turn=1
    while game_status != 'quit':
        for event in pygame.event.get():
            if event.type == QUIT:
                game_status = 'QUIT'
                pygame.quit()
                sys.exit()

            if event.type == START_SCREEN:
                draw_start_screen()

            if event.type == CHOOSE_PKMN:
                game_status='CHOOSE_PKMN'
                potrait_rect_list = pkmn_selection_screen(player1choice,player2choice)
            
            if event.type == BATTLE:
                game_status='BATTLE'
                player1pokemon,player2pokemon,player1pokemonbase,player2pokemonbase = \
                      initialize_player_pokemon(player1choice,player2choice)
                player1pokemon,player2pokemon = initialize_moves(player1pokemon,player2pokemon)
                currentpokemon, opposingpokemon, turn = turn_handler(player1pokemon,player2pokemon,turn)

                draw_battle_screen(currentpokemon, opposingpokemon)

                move_text_rect_list = show_moves(currentpokemon)

                
            if event.type == KEYDOWN:
                if event.key==K_SPACE and game_status == 'START_SCREEN':
                    pygame.event.post(pygame.event.Event(CHOOSE_PKMN))
                if game_status == 'CHOOSE_PKMN':
                    player1choice,player2choice = take_user_input(event,player1choice,player2choice)
                    
                    if event.key == K_RETURN and player1choice != 'Choose Pokemon' and player2choice != 'Choose Pokemon':  #Pressing Enter the Battle will begin
                        pygame.event.post(pygame.event.Event(BATTLE))               

                    #if player1choice != 'Choose Pokemon' and player2choice != 'Choose Pokemon':
                        #pygame.event.post(pygame.event.Event(BATTLE))

            if event.type == MOUSEBUTTONDOWN:
                if game_status == 'START_SCREEN':
                    pygame.event.post(pygame.event.Event(CHOOSE_PKMN))
                if game_status == 'CHOOSE_PKMN':
                    i = 1
                    for potrait_rect in potrait_rect_list:
                        if potrait_rect.collidepoint(event.pos):
                                player1choice,player2choice = set_player_choice(int(str(i)[-1]),player1choice,player2choice)    
                                #the int(str(i[-1])) is to take last digit of every number since machamp is 10th                         
                        i+=1
                if game_status == 'BATTLE':
                    move_chosen_no = 0
                    for move_text_rect in move_text_rect_list:
                        if move_text_rect.collidepoint(event.pos):

                            turn_damage, turn = currentpokemon.perform_attack(move_chosen_no, opposingpokemon,turn)
                            pygame.event.post(pygame.event.Event(BATTLE))
                        move_chosen_no+=1
                        


        pygame.display.update()
        CLOCK.tick(FPS)


if __name__=='__main__':
    main()
#print(pkmn_stats)
#print()
#print(type_matchups)

#player1=Pokemon(pkmn_stats.loc[0,'Name':'Defense'],pkmn_stats.loc[0,'Type'],pkmn_stats.loc[0,'Move1':'Move4'])

