import random
import argparse
import sys
comp_score = 0
user_score = 0

ROCK =1
PAPER =3
SCISSORS = 2

RULES = ({'name': 'rock', 'beats': SCISSORS,'id': ROCK},
          {'name': 'scissors','beats': PAPER,'id': SCISSORS},
          {'name': 'paper', 'beats': ROCK,'id': PAPER}
          )
          
parser = argparse.ArgumentParser(description='Rock Paper Scisors')
#parser.add_argument('choice',default=None)
parser.add_argument('-r',dest='count',default=False,type=int)

def play(choice=None):
    global comp_score
    global user_score
    if not choice:
        choice = random.randint(1,3)
    
    comp = random.randint(1,3)
    print '\n%s vs %s' % (RULES[choice-1]['name'], RULES[comp-1]['name'])
    if RULES[choice-1]['beats'] == comp:
        print 'Player won!'
        user_score +=1
    elif RULES[choice-1]['id'] == comp:
        print 'Tie!'
    else:
        print 'Player Lost!'
        comp_score +=1 
    print 'Score is: Player %s Computer %s' % (str(user_score),str(comp_score))
        
        

if len(sys.argv) >1: 
    arg = parser.parse_args(sys.argv[1:])
    for n in range(arg.count):
        play()
else:
    while True:
        print '\nSelect play:\n-----------------------------'
        for name in RULES:
            print str(name['id'])+' '+name['name']
        inp = raw_input('Choice: ')
        play(choice=int(inp))
        
        
                                                   
    

