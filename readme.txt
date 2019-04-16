Using Breadth first search to go through a maze.

The algorithm reference: https://blog.csdn.net/raphealguo/article/details/7523411

Demon:
>>>python BFS_Robot_movethrough_Maze.py

current maze(you can modify it in helper.py):

[[3, 2, 2, 2, 2, 2, 2, 2, 1],
 [0, 0, 2, 2, 2, 2, 2, 0, 0],
 [2, 0, 0, 2, 2, 2, 0, 0, 2],
 [2, 2, 0, 0, 2, 0, 0, 2, 2],
 [2, 2, 2, 0, 0, 0, 2, 2, 2]]
Desmontrate: if we put the robot in position 0,8, you should input position '(0,
8)'
Then you can see the action route like this:
Find the StoreHouse in step 16,location(0, 0).
The route table is saved at: ~/(0, 8).csv