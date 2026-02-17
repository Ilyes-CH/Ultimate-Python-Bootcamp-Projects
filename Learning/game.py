 # Rock Paper Scissor

# Player blueprint
player = {
    'username' : '',
    'age' : None,
    'score' : 0,
    'wins' : 0,
    'losses' :0,
}


#Create 2 players
player_one_name = input('enter player one name: ')
player_one_age= int(input('enter player one age: '))
player_two_name = input('enter player two name: ')
player_two_age = int(input('enter player two age: '))


#Age Restriction
if player_one_age < 10 or player_two_age < 10:
    print('Age Must Be 10 or Higher')
    player_one_age= int(input('enter player one age: '))
    player_two_age = int(input('enter player two age: '))


player_one = player.copy()
player_one.update({
    'username': player_one_name,
    'age' : player_one_age
})
player_two = player.copy()
player_two.update({
    'username': player_two_name,
    'age' : player_two_age
})
print(player_one)
print(player_two)

# Game Begin

tries = 0
max_tries = 3
print('########################################################################')
print('''
▗▄▄▖  ▄▄▄  ▗▞▀▘█  ▄     ▗▄▄▖ ▗▞▀▜▌▄▄▄▄  ▗▞▀▚▖ ▄▄▄      ▗▄▄▖▗▞▀▘▄  ▄▄▄  ▄▄▄  ▄▄▄   ▄▄▄ 
▐▌ ▐▌█   █ ▝▚▄▖█▄▀      ▐▌ ▐▌▝▚▄▟▌█   █ ▐▛▀▀▘█        ▐▌   ▝▚▄▖▄ ▀▄▄  ▀▄▄  █   █ █    
▐▛▀▚▖▀▄▄▄▀     █ ▀▄     ▐▛▀▘      █▄▄▄▀ ▝▚▄▄▖█         ▝▀▚▖    █ ▄▄▄▀ ▄▄▄▀ ▀▄▄▄▀ █    
▐▌ ▐▌          █  █     ▐▌        █                   ▗▄▄▞▘    █                      
                                                                                                                                                                                             
''')

print('########################################################################')


while tries <= max_tries:
   
    player_one_move = input(f'Your Move {player_one['username']}: ')
    player_two_move = input(f'Your Move Player {player_two['username']}: ')
    if player_one_move.lower() == player_two_move.lower() :
        print('TIE')
        player_one['score'] +=  1
        player_two['score'] += 1
    elif player_one_move.lower()== 'rock' and player_two_move.lower() == 'paper':
        print('Player Two Won')
        player_two['wins']+= 1
        player_one['losses']+= 1
        player_two['score'] +=1
    elif player_one_move.lower()== 'paper' and player_two_move.lower() == 'rock':
        print('Player One Won')
        player_one['wins']+= 1
        player_two['losses']+= 1
        player_one['score'] +=1
    elif player_one_move.lower()== 'paper' and player_two_move.lower() == 'scissor':
        print('Player Two Won')
        player_two['wins']+= 1
        player_one['losses']+= 1
        player_two['score'] +=1
    elif player_one_move.lower()== 'scissor' and player_two_move.lower() == 'paper':
        print('Player One Won')
        player_one['wins']+= 1
        player_two['losses']+= 1
        player_one['score'] +=1
    elif player_one_move.lower()== 'scissor' and player_two_move.lower() == 'rock':
        print('Player Two Won')
        player_two['wins']+= 1
        player_one['losses']+= 1
        player_two['score'] +=1
    elif player_one_move.lower()== 'rock' and player_two_move.lower() == 'scissor':
        print('Player Onw Won')
        player_one['wins']+= 1
        player_two['losses']+= 1
        player_one['score'] +=1
    tries += 1

  

    if tries == 3:
        print('Game Over')
        if player_one['score'] > player_two['score']:
            print('Player One Is the WINNER')
            print(f'Score : {player_one["score"]}')
            break
        elif player_two['score'] > player_one['score']:
            print('Player Two Is the WINNER')
            print(f'Score : {player_two["score"]}')
            break
        else:
            print('TIE Game')

            print(f'Player One Score : {player_one["score"]}')
            print(f'Player Two Score : {player_two["score"]}')
            break
