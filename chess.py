# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 14:55:27 2019

@author: Dell
"""
import string
import numpy as np
import re
import random
import time

#timing
t1 = time.time()

computer_players = 1

piece_values = {"Pn":10,"Kn":30,"Bp":30,"Rk":50,"Qn":90,"Kg":900}

def Board():
    return [['Rk1','Kn1','Bp1','Kg1','Qn1','Bp1','Kn1','Rk1'],
            ['Pn1','Pn1','Pn1','Pn1','Pn1','Pn1','Pn1','Pn1'],
            [' X ',' X ',' X ',' X ',' X ',' X ',' X ',' X '],
            [' X ',' X ',' X ',' X ',' X ',' X ',' X ',' X '],
            [' X ',' X ',' X ',' X ',' X ',' X ',' X ',' X '],
            [' X ',' X ',' X ',' X ',' X ',' X ',' X ',' X '],
            ['Pn2','Pn2','Pn2','Pn2','Pn2','Pn2','Pn2','Pn2'],
            ['Rk2','Kn2','Bp2','Kg2','Qn2','Bp2','Kn2','Rk2']]    

def Piece(board,square):
    """
    returns the piece in that square
    """
    if type(square) == str:
        square = (string.ascii_uppercase.index(square[0]),int(square[1])-1)
    return board[square[1]][square[0]] # finds piece type

def Pawn_taking(piece,current,target):
    """
    returns true if pawn is moving 1 space diagonally forward, else false
    """
    current,target = (string.ascii_uppercase.index(current[0]),int(current[1])-1),(string.ascii_uppercase.index(target[0]),int(target[1])-1)  
    if piece[-1] == '1': #player1
        if current[1] > target[1]: #Trying to move pawn backwards
            return False
    else: #player2
        if current[1] < target[1]: #Trying to move pawn backwards
            return False
    return abs(current[0] - target[0]) == abs(current[1] - target[1]) and abs(current[0] - target[0]) == 1 #pawn can move diagonally by 1 space


def Legal_move(board, piece, current, target):
    """
    uses python numbering (0,0 origin)
    returns True if move if legal, else false
    """
    alpha_current,alpha_target = current,target
    current,target = (string.ascii_uppercase.index(current[0]),int(current[1])-1),(string.ascii_uppercase.index(target[0]),int(target[1])-1)  
    def Pawn(): 
        if Piece(board,alpha_current)[-1] != Piece(board,alpha_target)[-1] and Piece(board,alpha_target) != ' X ': #the piece is a pawn and current and target pieces are from different players (pawn is taking)
            return Pawn_taking(piece,alpha_current,alpha_target)
        else:
            if piece[-1] == '1': #player1
                if current[1] > target[1]: #Trying to move pawn backwards
                    return False
            else: #player2
                if current[1] < target[1]: #Trying to move pawn backwards
                    return False
            if current[1] == 1 or current[1] == 6: #prawn on 2nd rank
                return (current[0] == target[0] and target[1] == current[1]+2) or (current[0] == target[0] and target[1] == current[1]+1) or (current[0] == target[0] and target[1] == current[1]-2) or (current[0] == target[0] and target[1] == current[1]-1) #pawn can move forward 2 ranks so long as same letter (updated to allow for player 2 (-1,-2)
            else:
                return (current[0] == target[0] and target[1] == current[1]+1) or (current[0] == target[0] and target[1] == current[1]-1) #pawn can move forward 1 ranks so long as same letter (updated to allow for player 2 (-1))
                
    def Rook():
        return current[0] == target[0] or current[1] == target[1] #rook can move as long as either letter or rank is the same, not both
    
    def Bishop():
        return abs(current[0] - target[0]) == abs(current[1] - target[1]) #Bishop can move so long as difference between letters and rank are equal    
        
    def Knight():
        return (abs(current[0] - target[0]) == 2 and abs(current[1] - target[1]) == 1) or (abs(current[0] - target[0]) == 1 and abs(current[1] - target[1]) == 2) #Knight can move so long as difference between letters is 2 and difference between rank is 1 or vice versa
        
    def Queen():
        return Bishop() or Rook() #Queen can move anywhere a bishop or rook can
    
    def King():
        return abs(current[0] - target[0]) == 1 and abs(current[1] - target[1]) == 1 #difference between letters is 1 or difference between rank is 1

    d = {'Kg':King(),'Qn':Queen(),'Bp':Bishop(),'Kn':Knight(),'Rk':Rook(),'Pn':Pawn()}
    
    return d[piece[:-1]]

#testing
#squares = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8']
#for i in range(1000):
#    p = "Kn1"
#    a,b = squares[random.randint(0,len(squares)-1)],squares[random.randint(0,len(squares)-1)]
#    if Legal_move(p,a,b):
#        print (a,b)
#        print (Legal_move(p,a,b))

def Route(current,target):
    """
    returns a list of squares through which a move would go
    list includes the current and target squares
    uses python numbering (0,0 origin)
    *Cannot be used to find route of a Knight*
    """    
    current,target = (string.ascii_uppercase.index(current[0]),int(current[1])-1),(string.ascii_uppercase.index(target[0]),int(target[1])-1)  
        
    if abs(current[0]-target[0]) > 0 and abs(current[1]-target[1]) == 0: #horizontal
        return [(i,target[1]) for i in range(current[0],target[0]+np.sign(target[0]-current[0]),+np.sign(target[0]-current[0]))]
        
    elif abs(current[1]-target[1]) > 0 and abs(current[0]-target[0]) == 0: #vertical
        return [(target[0],i) for i in range(current[1],target[1]+np.sign(target[1]-current[1]),+np.sign(target[1]-current[1]))]
         
    elif abs(current[1]-target[1]) > 0 and abs(current[0]-target[0]) > 0: #diagonal
        return list(zip([i for i in range(current[0],target[0]+np.sign(target[0]-current[0]),np.sign(target[0]-current[0]))],[i for i in range(current[1],target[1]+np.sign(target[1]-current[1]),np.sign(target[1]-current[1]))]))
 

def Target_accessible(board,current,target):
    """
    checks to see if target is free and accessible (players own pieces are not in way)
    uses python numbering (0,0 origin)
    returns the target square if not impeded
    returns 1 if move impeded by own piece, 2 if move impeded by opponents piece. 
    if piece is a knight, returns the target square if free or contains opponents piece
    if target contains own piece, returns 1 
    """  
    
    piece = Piece(board,current)
    if piece[:-1] == 'Kn':
        t_alphanumeric = target #save the alphanumeric  target square references (e.g. A3)
        current,target = (string.ascii_uppercase.index(current[0]),int(current[1])-1),(string.ascii_uppercase.index(target[0]),int(target[1])-1)  
        if board[target[1]][target[0]][-1] == piece[-1] and board[target[1]][target[0]] != ' X ': #target square occupied by own piece
            return 1
        else:
            return t_alphanumeric #return alphanumic reference 
    else:
        for i in Route(current,target)[1:-1]: #iterate through route (not including current position or target square)
            if Piece(board,i)[-1] == piece[-1] and Piece(board,i) != ' X ': #move impeded by own piece
                return 1
            elif Piece(board,i)[-1] != piece[-1] and Piece(board,i) != ' X ': #move impeded by opponents piece
                return 2
        if piece[-1] == Piece(board,target)[-1]: #if current piece and target piece are the same player's pieces
            return 1
        return target


def Update_board(board, current, target):
    """
    updates board to move the pieces
    uses python numbering (0,0 origin)
    """
    piece = Piece(board,current)
    current,target = (string.ascii_uppercase.index(current[0]),int(current[1])-1),(string.ascii_uppercase.index(target[0]),int(target[1])-1)  
    board[current[1]][current[0]] = ' X ' #replaces current with ' X '
    board[target[1]][target[0]] = piece #replaces target with piece from current
    return board
    
#play
def Play(board,taken,current,target):
    """
    if move is good it returns an updated board and taken list after the move has been made
    if move cannot be made it prints a message and returns the original board and taken list
    taken is a list of pieces that have been taken from either side
    """
    piece = Piece(board,current)
     
    pawn_taking,legal_move = False,False
    if piece[:-1] == "Pn" and piece[-1] != Piece(board,target)[-1] and Piece(board,target) != ' X ': #the piece is a pawn and current and target pieces are from different players (pawn is taking)
        pawn_taking = Pawn_taking(piece,current,target)
    else:
        legal_move = Legal_move(board,piece,current,target)

    if legal_move or pawn_taking: #move is legal
        if Target_accessible(board,current,target) == target: #target is accessible
            if piece[-1] != Piece(board,target)[-1] and Piece(board,target) != ' X ':
                taken.append(Piece(board,target))
            board = Update_board(board,current,target)
        else:
            if Target_accessible(board,current,target) == 1: #meets player's own piece
                if computer_players != 2: # computers are not playing each other
                    print ("You're own piece is in the way.")
                return None 
            elif Target_accessible(board,current,target) == 2: #collides with piece before reaching target and current piece is not a knight
                if computer_players != 2: # computers are not playing each other
                    print ("The opponent's piece is in the way")
                return None               
            
    else:
        print ("That move isn't legal")
        return None
    
    d = {'Kg':"King",'Qn':"Queen",'Bp':'Bishop','Kn':'Knight','Rk':'Rook','Pn':'Pawn'}
    print ("")
    print ("{} has moved their {} from {} to {}".format(player,d[piece[:-1]],current,target))
    return board,taken


def Exit():
    """
    function prints exit message
    """
    print ("")
    return "You are exiting the game"

def Player_piece(board,current,player):
    """
    checks to see if the piece being moved is the player's own
    returns True if it is the player's own piece
    returns False if it is the oppenents piece or an empty square
    """
    piece = Piece(board,current)
    if piece[-1] == player[-1]:
        return True
    else:
        if piece == ' X ':
            print ("")
            print ("You have selected an empty square.")
            return False
        else:
            print ("")
            print ("You are trying to move the opponent's piece.")
            return False
        
def player_points(board):
    """
    returns the scores of player1 and player 2 by summing the value of their pieces
    """
    p1_total = 0
    p2_total = 0
    for row in board:
        for square in row:
            if square[-1] == '1': #player1 
                p1_total += piece_values[square[:2]]
            elif square[-1] == '2': #player2
                p2_total += piece_values[square[:2]]
    return p1_total,p2_total

print (player_points(Board()))
    
        
def Computer(board,player):
    """
    returns a tuple containing a current and target 
    creates a  list of possible, legal and accessible moves
    """
    
    comp_pieces = []
    potential_targets = []
    opponent = "player" + str(abs(int(player[-1])-3)) # defines the opponent player from the current player past into the function
    for a,b in enumerate(board): 
        for y,z in enumerate(b): 
            if z[-1] == player[-1]: #if piece in square is computer's own 
                alpha_ref = string.ascii_uppercase[y] + str(a+1) #changes 0,0 coordinate to alphanumic reference (e.g. A1)
                comp_pieces.append(alpha_ref) #list of squares in which computer pieces are located
            else: #squares without computer's pieces in
                alpha_ref = string.ascii_uppercase[y] + str(a+1) #changes 0,0 coordinate to alphanumic reference (e.g. A1)
                potential_targets.append(alpha_ref) #list of squares in which computer pieces are not located
               
    potential_moves = [(current,target) for current in comp_pieces for target in potential_targets if Legal_move(board,Piece(board,current),current,target) and Target_accessible(board,current,target) == target] #list of possible, legal and accessible (current, target) tuples 
    
    taking_moves = [(current,target) for current,target in potential_moves if Piece(board,target)[-1] == opponent[-1]]
    print (taking_moves)
    
    if taking_moves: #if it is possible to take an opponents piece
        return taking_moves[random.randint(0,len(taking_moves)-1)]
    else:
        return potential_moves[random.randint(0,len(potential_moves)-1)]
         
board = Board()
taken = []
player = "player1"
while 'Kg1' not in taken and 'Kg2' not in taken:
    #display board
    print ("")
    print ('     A   ','  B   ','  C   ','  D   ','  E   ','  F   ','  G   ','  H   ')  
    print ("")
    for a,b in enumerate(board):
        print (a+1,b,a+1)
    print ("")
    print ('     A   ','  B   ','  C   ','  D   ','  E   ','  F   ','  G   ','  H   ')  
    print ("")
    
    #display taken pieces
    print ("Taken pieces = {}".format(taken))
    print ("")
    
    print ("It's {}'s turn".format(player))
    
    #checking for any faults in input
    while True:
        #computer input
        if computer_players == 1 and player == "player2": ##Player 2 is computer player
            (current,target) = Computer(board,player)
        elif computer_players == 2:
            (current,targer) = Computer(board,player)
        else:            
            #player input
            current,target = input("Please input which square you'd like to move from: ").upper(),input("Please input which square you'd like to move to: ").upper()
        #checking for valid input
        if not re.search("[A-H][1-8]",current) or not re.search("[A-H][1-8]",target): #input is in correct format
            if current == 'EXIT' or target == "EXIT": #allows for exit calls
                break
            else:
                print ("")
                print ("Your input was not valid. Please input a reference between 'A1-H8'")
                continue
            
        #check to see if that's your piece
        if not Player_piece(board,current,player):
            continue
        
        #play game
        #if it doesn't return a value, returns to top of while loop
        if not Play(board,taken,current,target):
            continue
        
        break
            
    #exit door
    if current == 'EXIT' or target == 'EXIT':
        print (Exit())
        break
               
    #change player
    if player == 'player1':
        player = 'player2'
    else:
        player = 'player1'
    
else:
    print ("")
    print ("Taken pieces = {}".format(taken))
    print ("The king is dead")
    if taken[-1] == 'Kg1':
        print ("Player 2 wins!")
    else:
        print ("Player 1 wins!")
        



#timing
t2 = time.time()


'''
#to do


display board function
computer
check and check mate
pawn taking in legal move 
target accessible (knights and testing)


'''

#    squares = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8']
#    return squares[random.randint(0,len(squares)-1)],squares[random.randint(0,len(squares)-1)]





