import pygame
from pygame.locals import *
import numpy as np
import pandas as pd
import random as rnd
import sys 

pygame.init()

#Load Dataframes
pkmn_stats = pd.read_csv('pokemon_stats.csv') #Dataframe of all (10 included) Pokemon with HP,Attack,Defense,Type and Moves.
pkmn_stats.loc['Choose Pokemon','Name']='Choose Pokemon'
type_matchups = pd.read_csv('type_matchups.csv').T #Stores all 12 types(included), with their weaknesses,resistances and immunities. 
type_matchups.columns = ["weaknesses","resistances","immunities"] #assigns columns after transposing it
moves_df=pd.read_csv('moves.csv') #stores moves with type, damage, and other parameters
moves_df.index=moves_df.loc[:,'Name'] 

#Display
WIDTH,HEIGHT = 800,600
DISPLAY_SIZE = (WIDTH,HEIGHT)
DISPLAY = pygame.display.set_mode(DISPLAY_SIZE)
pygame.display.set_caption("POKEMON GAME")

#Fonts
font60 = pygame.font.Font("Pixeltype.ttf",60)
font100 = pygame.font.Font("Pixeltype.ttf",100)

#Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

#FPS
FPS = 60
CLOCK = pygame.time.Clock()

#START SCREEN
pkmn_background = pygame.image.load("gengar_pixels.jpeg").convert_alpha() #Pixel Art of a Gengar for the Start Screen, Spooky... 
pkmn_background = pygame.transform.scale(pkmn_background, DISPLAY_SIZE)
pkmn_logo = pygame.image.load("pkmn_logo.png").convert_alpha() #Transparent, Black Pokemon Logo
#pkmn_logo = pygame.transform.scale(pkmn_logo, (100,100))
blue_sky=pygame.image.load("blue_sky.jpg").convert() #Blue Sky for the PKMN selection screen.
blue_sky=pygame.transform.scale(blue_sky, DISPLAY_SIZE) 


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

    player1text=font60.render(f"Player1: {pkmn_stats.loc[player1choice,'Name']}",0,'White') #render() has 3 required arguments:
    player2text=font60.render(f"Player2: {pkmn_stats.loc[player2choice,'Name']}",0,'White') #1.Text to render
                                                                                            #2.Whether to Anti-Alias
                                                                                            #3.Color of text
    DISPLAY.blit(blue_sky,(0,0))
    DISPLAY.blit(toptext,toptextrect)
    DISPLAY.blit(player1text,(10,100))
    DISPLAY.blit(player2text,(10,150))
    
    for i in range(1,6):
        pokemon_potrait = pygame.image.load(f'potraits/{i}.png').convert_alpha()
        pokemon_potrait = pygame.transform.scale(pokemon_potrait,(120,120))
        pokemon_recttop=pokemon_potrait.get_rect(center=(WIDTH*i/5-WIDTH/10,300))
        DISPLAY.blit(pokemon_potrait,pokemon_recttop)
    for i in range(6,11):
        pokemon_potrait = pygame.image.load(f'potraits/{i}.png').convert_alpha()
        pokemon_potrait = pygame.transform.scale(pokemon_potrait,(120,120))
        pokemon_rect=pokemon_potrait.get_rect(center=(WIDTH*(i-5)/5-WIDTH/10,500))
        DISPLAY.blit(pokemon_potrait,pokemon_rect)

    pygame.display.update()
    
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
        move=Move(*moves_df.loc[move,'Name':'Turn_no'],moves_df.loc[move,'Status Effect':'Status Chance'])
        player1moves.append(move)
    player1pokemon.moves=player1moves
    
    player2moves=[]
    for move in player2pokemon.moves:
        move=Move(*moves_df.loc[move,'Name':'Turn_no'],moves_df.loc[move,'Status Effect':'Status Chance'])
        player2moves.append(move)
    player2pokemon.moves=player2moves
    
    return player1pokemon,player2pokemon

class Pokemon:
    def __init__(self,name,HP,attack,defense,type_,moves,status=None):
        self.name=name
        self.HP=HP
        self.attack=attack
        self.defense=defense
        self.type_ = type_
        self.moves = moves
        self.status = status

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
                pkmn_selection_screen(player1choice,player2choice)
            
            if event.type == BATTLE:
                game_status='BATTLE'
                player1pokemon,player2pokemon = initialize_player_pokemon(player1choice,player2choice)
                player1pokemon,player2pokemon = initialize_moves(player1pokemon,player2pokemon)
                
                


            if event.type == KEYDOWN:
                if event.key==K_SPACE and game_status == 'START_SCREEN':
                    pygame.event.post(pygame.event.Event(CHOOSE_PKMN))
                if game_status == 'CHOOSE_PKMN':
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
                    
                    if player1choice != 'Choose Pokemon' and player2choice != 'Choose Pokemon':
                        pygame.event.post(pygame.event.Event(BATTLE))

        pygame.display.update()
        CLOCK.tick(FPS)


if __name__=='__main__':
    main()
#print(pkmn_stats)
#print()
#print(type_matchups)

#player1=Pokemon(pkmn_stats.loc[0,'Name':'Defense'],pkmn_stats.loc[0,'Type'],pkmn_stats.loc[0,'Move1':'Move4'])

