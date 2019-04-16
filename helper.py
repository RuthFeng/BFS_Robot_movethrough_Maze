import time

'''
0:null node,walkable
1:robot position,walkable
2:block,un-walkable
3:storehouse,target
'''
MAZE = [
    [3,2,2,2,2,2,2,2,1],
    [0,0,2,2,2,2,2,0,0],
    [2,0,0,2,2,2,0,0,2],
    [2,2,0,0,2,0,0,2,2],
    [2,2,2,0,0,0,2,2,2]]


def fetch_maze():
    return MAZE

def main ():
    fetch_maze()

# Call to main function to run the program
if __name__ == "__main__":
    main()