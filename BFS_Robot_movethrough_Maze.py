import pandas as pd
import copy
import argparse
import helper

env_data = helper.fetch_maze()


def is_move_valid_visited(env_data,visit_map,loc,act):
    """
    Judge wether the robot can take action act
    at location loc.
    
    Keyword arguments:
    env -- list, the environment data
    loc -- tuple, robots current location
    act -- string, robots meant action
    """
    nextloc=list(loc)
    if act=='u':
        nextloc[0]=nextloc[0]-1

    elif act=='d':
        nextloc[0]=nextloc[0]+1

    elif act=='r':
        nextloc[1]=nextloc[1]+1

    elif act=='l':
        nextloc[1]=nextloc[1]-1

    else:

        return False
    


    if (nextloc[0] in range(len(env_data))) and (nextloc[1] in range(len(env_data[0]))):
        if env_data[nextloc[0]][nextloc[1]]==0 or env_data[nextloc[0]][nextloc[1]]==1 or env_data[nextloc[0]][nextloc[1]]==3:

            if visit_map[nextloc[0]][nextloc[1]]==0 or visit_map[nextloc[0]][nextloc[1]]==1 or visit_map[nextloc[0]][nextloc[1]]==3:

                return True
            else:

                return False
        else:

            return False
    else:
        return False

def valid_novisit_actions(env_data,visit_map,loc):
    valid_action=[]
    '''
    Follow u,d,r,l direction to move around
    '''
    for i in ['u','d','r','l']:
        if is_move_valid_visited(env_data,visit_map,loc,i):
            valid_action.append(i)
    return valid_action

def get_valid_neighbor_loc(loc,action_list):
    neighbor_list=list()    
    '''
    Follow u,d,r,l direction to move around
    '''
    for i in action_list:
        new_loc=list(loc)
        if i=='u':
            new_loc[0]=new_loc[0]-1            
        elif i=='d':
            new_loc[0]=new_loc[0]+1
        elif i=='r':
            new_loc[1]=new_loc[1]+1
        elif i=='l':
            new_loc[1]=new_loc[1]-1

        neighbor_list.append((new_loc[0],new_loc[1]))
    return neighbor_list

def move_robot(loc, act):
    move_dict ={
    'u': (-1,0),
    'd': (1,0),
    'l': (0,-1),
    'r': (0,1)
    }
    return loc[0] + move_dict[act][0], loc[1] + move_dict[act][1]


def bfs_move_robot(env_data,visit_map,loc,act_list,route_table):
#algorithm reference: https://blog.csdn.net/raphealguo/article/details/7523411     
    for act in act_list:
        new_loc=list(loc)
        if act=='u':
            new_loc[0]=new_loc[0]-1
        elif act=='d':
            new_loc[0]=new_loc[0]+1
        elif act=='r':
            new_loc[1]=new_loc[1]+1
        elif act=='l':
            new_loc[1]=new_loc[1]-1
        mark_visit(visit_map,(new_loc[0],new_loc[1]),'gray')
        route_table=route_table.append(pd.DataFrame(data={'source_loc':[(list(loc)[0],list(loc)[1])],'move_direct':act,'next_loc':[(new_loc[0],new_loc[1])],'route_type':'forward'}),ignore_index=True)
        if env_data[new_loc[0]][new_loc[1]]==3:
            return route_table
        else:
            Source_loc=new_loc
            new_loc=move_back_robot(new_loc,act)
            act=roll_back_direction(act)
            route_table=route_table.append(pd.DataFrame(data={'source_loc':[(Source_loc[0],Source_loc[1])],'move_direct':act,'next_loc':[(new_loc[0],new_loc[1])],'route_type':'backward'}),ignore_index=True)
            
            continue
    return route_table

def move_back_robot(loc,act):
    '''Rollback need not check visit_map'''
    new_loc=list(loc)
    if act=='u':
        new_loc[0]=new_loc[0]+1
    elif act=='d':
        new_loc[0]=new_loc[0]-1
    elif act=='r':
        new_loc[1]=new_loc[1]-1
    elif act=='l':
        new_loc[1]=new_loc[1]+1    
    return (new_loc[0],new_loc[1])

def roll_back_direction(act):
    '''Rollback need not check visit_map'''
    if act=='u':
        new_act='d'
    elif act=='d':
        new_act='u'
    elif act=='l':
        new_act='r'
    elif act=='r':
        new_act='l'
    return new_act

def mark_visit(visit_map,loc,color):
    new_loc=list(loc)
    if color=='dark':
        visit_map[new_loc[0]][new_loc[1]]=4
    elif color=='gray':
        visit_map[new_loc[0]][new_loc[1]]=5
    else:
        print('Only accept color:dark or gray!')


def trace_route(route_table,initial_loc,from_loc,to_loc):
    back_route=pd.DataFrame(columns=['source_loc','move_direct','next_loc','route_type'])
    forward_route=pd.DataFrame(columns=['source_loc','move_direct','next_loc','route_type'])
    forward_route=forward_route.append(route_table[route_table.route_type=='forward'],ignore_index=True)

    s_flag=0
    d_flag=0
    if from_loc==to_loc:

        return
    else:
        s_loc=from_loc
        d_loc=to_loc
        while 1:


            if s_loc==initial_loc or d_loc==initial_loc:
                if s_loc==initial_loc and d_loc==initial_loc:
                    break                    
                elif s_loc==initial_loc:

                    d_route=pd.DataFrame(columns=['source_loc','move_direct','next_loc','route_type']).append(forward_route[forward_route.next_loc==d_loc],ignore_index=True)
                    if s_flag==0:

                        s_route=pd.DataFrame(columns=['source_loc','move_direct','next_loc','route_type']).append(forward_route[(forward_route.source_loc==s_loc) & (forward_route.next_loc==d_loc)],ignore_index=True)

                        back_route=back_route.append(pd.DataFrame(data={'source_loc':[s_route.loc[0]['next_loc']],'move_direct':roll_back_direction(s_route.loc[0]['move_direct']),'next_loc':[s_route.loc[0]['source_loc']],'route_type':'backward'}),ignore_index=True)
                        s_flag+=1                      
                    back_route=back_route.append(pd.DataFrame(data={'source_loc':[d_route.loc[0]['source_loc']],'move_direct':d_route.loc[0]['move_direct'],'next_loc':[d_route.loc[0]['next_loc']],'route_type':'backward'}),ignore_index=True)
                    d_loc=d_route.loc[0]['source_loc']
                    
                elif d_loc==initial_loc:

                    if d_flag==0:

                        d_route=pd.DataFrame(columns=['source_loc','move_direct','next_loc','route_type']).append(forward_route[(forward_route.source_loc==s_loc) & (forward_route.next_loc==d_loc)],ignore_index=True)

                        back_route=back_route.append(pd.DataFrame(data={'source_loc':[d_route.loc[0]['source_loc']],'move_direct':d_route.loc[0]['move_direct'],'next_loc':[d_route.loc[0]['next_loc']],'route_type':'backward'}),ignore_index=True)
                        d_flag+=1
                    s_route=pd.DataFrame(columns=['source_loc','move_direct','next_loc','route_type']).append(forward_route[forward_route.next_loc==s_loc],ignore_index=True)

                    back_route=back_route.append(pd.DataFrame(data={'source_loc':[s_route.loc[0]['next_loc']],'move_direct':roll_back_direction(s_route.loc[0]['move_direct']),'next_loc':[s_route.loc[0]['source_loc']],'route_type':'backward'}),ignore_index=True)
                    
                    s_loc=s_route.loc[0]['source_loc']
            elif s_loc==d_loc:

                break
            else:
                s_route=pd.DataFrame(columns=['source_loc','move_direct','next_loc','route_type']).append(forward_route[forward_route.next_loc==s_loc],ignore_index=True)
                d_route=pd.DataFrame(columns=['source_loc','move_direct','next_loc','route_type']).append(forward_route[forward_route.next_loc==d_loc],ignore_index=True)


                back_route=back_route.append(pd.DataFrame(data={'source_loc':[d_route.loc[0]['source_loc']],'move_direct':d_route.loc[0]['move_direct'],'next_loc':[d_route.loc[0]['next_loc']],'route_type':'backward'}),ignore_index=True)
                back_route=back_route.append(pd.DataFrame(data={'source_loc':[s_route.loc[0]['next_loc']],'move_direct':roll_back_direction(s_route.loc[0]['move_direct']),'next_loc':[s_route.loc[0]['source_loc']],'route_type':'backward'}),ignore_index=True)
                
                s_loc=s_route.loc[0]['source_loc']
                d_loc=d_route.loc[0]['source_loc']
            
     
        s_loc=from_loc       

        while 1:

            if s_loc==to_loc:

                return route_table
            else:

                
                s_route=pd.DataFrame(columns=['source_loc','move_direct','next_loc','route_type']).append(back_route[back_route.source_loc==s_loc],ignore_index=True)

                route_table=route_table.append(s_route,ignore_index=True)                
                s_loc=s_route.loc[0]['next_loc']  
        
    
def to_destination_actions(env_data,current_loc):
    dest_exist=0
    route_file=str(current_loc)+'.'+'csv'

    '''Check if value 3 exists in maze'''
    for i in range(len(env_data)):
        dest_exist+=env_data[i].count(3)
        
    
    if dest_exist==1:
        '''if initial poisition is storehouse 3, return'''
        if env_data[list(current_loc)[0]][list(current_loc)[1]]==3:
            print('Current location is the StoreHouse,stop moving!')
            return
        else:
            '''Intial the BFS visit map, value 1/3/0 means the walkable unvisited nodes, color white; 4 means the visited nodes, color black; 5 means the to be visited nodes, color gray. Reference:https://blog.csdn.net/raphealguo/article/details/7523411 '''
            visit_map=copy.deepcopy(env_data)


            wait_queue=list([current_loc])

            old_loc=current_loc

            route_table=pd.DataFrame(columns=['source_loc','move_direct','next_loc','route_type'])


            while wait_queue:

                loc=wait_queue.pop(0) 
                
                loc_list=list(loc)

                mark_visit(visit_map,(loc_list[0],loc_list[1]),'dark')

                act_list=valid_novisit_actions(env_data,visit_map,loc_list)
                neighbor_list=get_valid_neighbor_loc(loc_list,act_list)
                                
                """when visit the next gray nodes, the robot needs to move from current root node to this node firstly, the route table will record the action"""
                
                if len(route_table)>1:
                    if route_table[route_table.source_loc==old_loc].reset_index().loc[0]['next_loc']!=loc:



                        route_table=trace_route(route_table,current_loc,old_loc,loc)               
                


                
                
                if env_data[list(loc)[0]][list(loc)[1]]==3:
                        print('Find the StoreHouse in step {},location{}.'.format(len(route_table),loc))
                        route_table.to_csv(route_file)
                        print('The route table is saved at: ~/'+route_file)
                        return
                if neighbor_list:
                    for neighbor in neighbor_list:
                        wait_queue.append(neighbor)


                    if len(neighbor_list)>1:

                        route_table=bfs_move_robot(env_data,visit_map,loc,act_list,route_table)

                        verify_loc=route_table.loc[len(route_table)-1].next_loc
                        if verify_loc!=wait_queue[0]:
                            route_table=trace_route(route_table,current_loc,verify_loc,wait_queue[0]) 

                        old_loc=loc

                    elif len(neighbor_list)==1:
                        one_loc=move_robot(loc,act_list[0])
                        old_loc=loc

                        mark_visit(visit_map,(one_loc[0],one_loc[1]),'gray')
                        route_table=route_table.append(pd.DataFrame(data={'source_loc':[(old_loc[0],old_loc[1])],'move_direct':act_list[0],'next_loc':[(one_loc[0],one_loc[1])],'route_type':'forward'}),ignore_index=True)
                        verify_loc=route_table.loc[len(route_table)-1].next_loc                     
                        
                        if verify_loc!=wait_queue[0]:
                            route_table=route_table.append(pd.DataFrame(data={'source_loc':[(one_loc[0],one_loc[1])],'move_direct':roll_back_direction(act_list[0]),'next_loc':[(old_loc[0],old_loc[1])],'route_type':'backward'}),ignore_index=True)
                        if env_data[list(one_loc)[0]][list(one_loc)[1]]==3:
                            print('Find the StoreHouse in step {},location{}.'.format(len(route_table),one_loc))
                            route_table.to_csv(route_file)
                            print('The route table is saved at: ~/'+route_file)
                            return                        
                else:
                    continue            
    else:
        print('Maze_map initial error,please assign only one destination point with value 3!')
        return   


   
def main ():
     print('current maze(you can modify it in helper.py): \n')
     print('['+str(env_data[0])+',')
     for line in env_data[1:-1]:
         print(' '+str(line)+',')
     print(' '+str(env_data[-1])+']')

     print('Desmontrate: if we put the robot in position 0,8, you should input position \'(0,8)\'')
     print('Then you can see the action route like this: ')
     to_destination_actions(env_data,(0,8))

     print('\n \n ***Now begin your test: ')
     x = input('enter robot_start_position,e.g: (4,4) :')     
     to_destination_actions(env_data,x)


# Call to main function to run the program
if __name__ == "__main__":
    main()