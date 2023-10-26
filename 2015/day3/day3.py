from collections import defaultdict


def load_input(filename):
    with open(filename, 'r') as f:
        line = next(f).strip()
    
    return line

if __name__ == '__main__':

    path = load_input('input')

    visits = defaultdict(int)

    posx, posy = 0, 0
    visits[(posx, posy)] = 1
    for dir in path[::2]:
        if dir == '>':
            posx += 1
        elif dir == '<':
            posx -= 1
        elif dir == '^':
            posy += 1
        elif dir == 'v':
            posy -= 1
        
        visits[(posx, posy)] += 1
    
    posx, posy = 0, 0
    for dir in path[1::2]:
        if dir == '>':
            posx += 1
        elif dir == '<':
            posx -= 1
        elif dir == '^':
            posy += 1
        elif dir == 'v':
            posy -= 1
        
        visits[(posx, posy)] += 1

    print('part2', len(visits))
            
