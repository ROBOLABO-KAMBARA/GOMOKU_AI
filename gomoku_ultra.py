# -*- coding: utf-8 -*-
import os
import numpy as np
import random
import glob
import sys
import copy
import heapq
#2018/06/19
#made by Kazunari Morita


P1 = 2 #先手:Player=0, COM>=1
P2 = 1 #後手

SCORE_SHOW = 0 #HIDDEN=0, SHOW=1

game_num = 100 #ゲーム回数

#色の定義
SPACE = 0
BLACK = 1
WHITE = 2
#盤面の大きさ
BOARD_SIZE = 15
#方向
VERTIC = 1 
HOLIZ = 2
R_OBLI = 3
L_OBLI = 4

class Stone_array:
        def __init__(self, pos_x, pos_y, dirc, pos, color):
            self.grid = [pos_x, pos_y]
            self.direction = dirc
            self.color = color
            self.array = [0,0,0,0,0]
            self.array[pos] = color
            self.stone_num = 1
        
        def get_score(self, next_turn):
            if(self.color == BLACK):
                if self.stone_num == 5:
                    return 9999999
                elif next_turn == BLACK and self.stone_num == 4:
                    return 999999
                if next_turn == BLACK:
                    return int(pow(10, self.stone_num-1)*3)
                else:
                    return int(pow(10, self.stone_num-1))

            elif(self.color == WHITE):
                if self.stone_num == 5:
                    return -9999999
                elif next_turn == WHITE and self.stone_num == 4:
                    return -999999
                if next_turn == WHITE:
                    return -int(pow(10, self.stone_num-1)*3)
                else:
                    return -int(pow(10, self.stone_num-1))
            return 0
        
        def add_stone(self):
            #石の追加
            return 0

        def print(self):
            print(self.grid, self.direction, self.color, self.array, self.stone_num)

class Gomokunarabe_tree:

    def __init__(self):
        self.name = os.path.splitext(os.path.basename(__file__))[0]
        self.enable_actions = np.arange(BOARD_SIZE*BOARD_SIZE)
        self.screen = np.zeros((BOARD_SIZE, BOARD_SIZE))
        self.stone_arrays = []

    def reset(self):
        """ 盤面の初期化 """
        # reset ball position
        self.screen = np.zeros((BOARD_SIZE, BOARD_SIZE),dtype=np.int8)

    def score(self, next_turn):
        score = 0
        score_sum = 0
        for array in self.stone_arrays:
            score = array.get_score(next_turn)
            if abs(score) == 9999999:
                return score
            score_sum += score

        return score_sum

    #勝った方のラベル返す(いたら)
    def winner(self):
        for array in self.stone_arrays:
            if array.stone_num == 5:
                if array.color == BLACK:
                    print ('先手勝利')
                    print ('\n\n')
                elif array.color == WHITE:
                    print ('後手勝利')
                    print ('\n\n')
                return array.color

        #引き分け判定
        if 0 not in self.screen:
            #盤面の描画
            # self.display_screen()
            print ('Draw')
            print ('\n\n')
            return 3
        return False

    def make_array(self, pos_y, pos_x, color):
        #stone_arrayを作る判定
        #縦の判定
        minus = 0
        plus = 0
        for i in range(1, 5):
            if (pos_x - i) < 0: break
            if self.screen[pos_x - i][pos_y] != 0: break
            minus -= 1
        for i in range(1, 5):
            if (pos_x + i)>=15: break
            if self.screen[pos_x + i][pos_y] != 0: break       
            plus += 1
        while ((plus - minus + 1) >= 5):
            self.stone_arrays.append(Stone_array(pos_x + minus , pos_y, VERTIC, -minus, color))
            minus += 1

        #横の判定
        minus = 0
        plus = 0
        for i in range(1, 5):
            if (pos_y - i)<0: break
            if self.screen[pos_x][pos_y-i] != 0: break
            minus -= 1
        for i in range(1, 5):
            if (pos_y + i)>=15: break
            if self.screen[pos_x][pos_y+i] != 0: break
            plus += 1
        while (plus - minus + 1) >= 5:
            self.stone_arrays.append(Stone_array(pos_x, pos_y + minus, HOLIZ, -minus, color))
            minus += 1

        #右斜め下方向の判定
        minus = 0
        plus = 0
        for i in range(1,5):
            if (pos_x - i)<0 or (pos_y - i)<0: break
            if self.screen[pos_x - i][pos_y - i] != 0: break
            minus -= 1
        for i in range(1,5):
            if (pos_x + i)>=15 or (pos_y + i)>=15: break
            if self.screen[pos_x + i][pos_y + i] != 0: break
            plus += 1
        while (plus - minus + 1) >= 5:
            self.stone_arrays.append(Stone_array(pos_x + minus, pos_y + minus, R_OBLI, -minus, color))
            minus += 1

        #左斜め下方向の判定
        minus = 0
        plus = 0
        for i in range(1,5):
            if (pos_x - i)<0 or (pos_y + i)>=15: break
            if self.screen[pos_x - i][pos_y + i] != 0: break
            minus -= 1
        for i in range(1,5):
            if (pos_x + i)>=15 or (pos_y - i)<0: break
            if self.screen[pos_x + i][pos_y - i] != 0: break
            plus += 1
        while (plus - minus + 1) >= 5:
            self.stone_arrays.append(Stone_array(pos_x + minus, pos_y - minus, L_OBLI, -minus, color))
            minus += 1

        #print("--arrays--")
        #for a in self.stone_arrays:
        #    a.print()

    def check_array(self, pos_y, pos_x, color):
        #stone_arrayの点検/更新
        i = 0
        while i < len(self.stone_arrays):
            a = self.stone_arrays[i]
            if(a.direction == VERTIC):
                if(pos_y == a.grid[1]):
                    if (pos_x - a.grid[0])<5 and (pos_x - a.grid[0])>=0:
                        if a.color == color:
                            if a.array[pos_x - a.grid[0]]==0:
                                a.array[pos_x - a.grid[0]] = color
                                a.stone_num += 1
                        else:
                            self.stone_arrays.remove(a)
                            i-=1
                            
            elif(a.direction == HOLIZ):           
                if(pos_x == a.grid[0]):                  
                    if (pos_y - a.grid[1])<5 and (pos_y - a.grid[1])>=0:
                        if a.color == color:
                            if a.array[pos_y - a.grid[1]]==0:
                                a.array[pos_y - a.grid[1]] = color
                                a.stone_num += 1
                        else:
                            self.stone_arrays.remove(a)
                            i-=1
                            
            elif(a.direction == R_OBLI):       
                if (pos_x - a.grid[0])==(pos_y - a.grid[1]):
                    if (pos_y - a.grid[1])<5 and (pos_y - a.grid[1])>=0 and (pos_x - a.grid[0])<5 and (pos_x - a.grid[0])>=0:
                        if a.color == color:
                            if a.array[pos_x - a.grid[0]]==0:
                                a.array[pos_x - a.grid[0]] = color
                                a.stone_num += 1
                        else:
                            self.stone_arrays.remove(a)
                            i-=1


            elif(a.direction == L_OBLI):       
                if (pos_x - a.grid[0])==-(pos_y - a.grid[1]):
                    if -(pos_y - a.grid[1])<5 and -(pos_y - a.grid[1])>=0 and (pos_x - a.grid[0])<5 and (pos_x - a.grid[0])>=0:
                        if a.color == color:
                            if a.array[pos_x - a.grid[0]]==0:
                                a.array[pos_x - a.grid[0]] = color
                                a.stone_num += 1
                        else:
                            self.stone_arrays.remove(a) 
                            i-=1
            i+=1

    def update(self, pos_x, pos_y, color):
        self.check_array( pos_x, pos_y, color)
        self.make_array( pos_x, pos_y, color)
        self.screen[pos_y][pos_x] = color
    
    def isEnd(self):
        return self.winner() 
        
        # return True    

    #先手のターン
    def p1_turn(self):
        print ('先手の番')

        if P1 > 0: #COM
            value, i, j = self.search_AI(1, 5, P1)
            p_x_pos = i
            p_y_pos = j
            print(value, i, j)
        else: #Player
            p_x_pos = input('select ball x pos > ')
            p_y_pos = input('select ball y pos > ')

        if int(p_x_pos) == 0:
            return 0
        while int(p_x_pos)<1 or int(p_x_pos)>15 or  int(p_y_pos)<1 or int(p_y_pos)>15 or self.screen[int(p_y_pos)-1][int(p_x_pos)-1] == 1 or  self.screen[int(p_y_pos)-1][int(p_x_pos)-1] == 2: 
            print ('please retry')
            p_x_pos = input('select ball x pos > ')
            p_y_pos = input('select ball y pos > ')

        self.update(int(p_x_pos)-1, int(p_y_pos)-1, 1)

    #後手のターン
    def p2_turn(self):
        print ('後手の番')
        
        if P2 > 0: #COM
            value, i, j = self.search_AI(2, 5, P2)
            p_x_pos = i
            p_y_pos = j
            print(value, i, j)
        else: #Player
            p_x_pos = input('select ball x pos > ')
            p_y_pos = input('select ball y pos > ')

        if int(p_x_pos) == 0:
            return 0
        while int(p_x_pos)<1 or int(p_x_pos)>15 or  int(p_y_pos)<1 or int(p_y_pos)>15 or self.screen[int(p_y_pos)-1][int(p_x_pos)-1] == 1 or  self.screen[int(p_y_pos)-1][int(p_x_pos)-1] == 2: 

            print ('please retry')
            p_x_pos = input('select ball x pos > ')
            p_y_pos = input('select ball y pos > ')
        self.update(int(p_x_pos)-1, int(p_y_pos)-1, 2)


    #AI
    def search_AI(self, turn , leaf_num, depth):
        if depth == 0:
            if turn == BLACK:
                return self.score(BLACK), 0, 0
            else:
                return self.score(WHITE), 0, 0
        
        move = []
        score_list = []
        start_flag = 1
        for i in range(15):
            for j in range(15):
                side_flag = 0
                for k in range(3):
                    for l in range(3):
                        if(i+(k-1)>=0 and i+(k-1)< 15 and j+(l-1)>=0 and j+(l-1)<15 and self.screen[i+(k-1)][j+(l-1)]!=0):
                            side_flag = 1
                if self.screen[i][j]==0 and side_flag==1:
                    start_flag = 0
                    b = copy.deepcopy(self)
                    #手を指す
                    b.update(j, i, turn)
                    #b.display_screen()
                    #print(v, j+1, i+1)
                    if turn == BLACK:
                        v = b.score(WHITE)
                        if v == 9999999:
                            return v, j+1, i+1
                    else:
                        v = b.score(BLACK)
                        if v < -9999999:
                            return v, j+1, i+1
                    score_list.append([v, b, [j+1, i+1]])
        v=0
        #上位leaf位を抽出
        if turn == BLACK:
            value = -100000000
            leaf_list = heapq.nlargest(leaf_num, score_list, key=lambda x:x[0])
            print('LofL', leaf_list)
            for leaf in leaf_list:
                v, a, b = leaf[1].search_AI(WHITE, leaf_num, depth-1)
                if value < v:
                    value = v
                    move = [leaf[2]]
                elif value == v:
                    move.append(leaf[2])
        else:
            value = 100000000
            leaf_list = heapq.nsmallest(leaf_num, score_list, key=lambda x:x[0])
            print('LofL', leaf_list)
            for leaf in leaf_list:
                v, a, b = leaf[1].search_AI(BLACK, leaf_num, depth - 1)
                if value > v:
                    value = v
                    move= [leaf[2]]
                elif value == v:
                    move.append(leaf[2])
        if start_flag == 1:
            return 0, 8, 8
        #print(move, ':' ,value)
        #print('.', end='')
        b = None
        m = random.choice(move)
        return value, m[0], m[1]
    
    #盤面の表示
    def display_screen(self):
        print ('    1 2 3 4 5 6 7 8 9 a b c d e f')
        for i in range(15):
            print(hex(i+1), end='')
            for j in range(15):
                # if i==0 and j==0:
                #     for k in range(1,16):
                #         print (str(k)+'　', end='')
                #     print ('\n',end='')
                if  self.screen[i][j]==0:
                    print (' +', end='')

                elif self.screen[i][j]==1:
                    print (' O', end='')

                elif self.screen[i][j]==2:
                    print (' X', end='')

            print ('\n', end='')
            
        print ('[先手]'+' O', '\t[後手]'+' X')
        print ('\n\n')

#メイン文
if __name__ == '__main__':

    p1_win = 0
    p2_win = 0
    draw = 0

    for i in range(game_num):
        win_judge = 0
        env = Gomokunarabe_tree()
        #盤面の描画
        env.display_screen()        

        # screen = np.zeros([15,15])
        while 1:

            #先手のターン
            env.p1_turn()
            
            #盤面の描画
            env.display_screen()

            win_judge = env.winner() 

            #勝敗判定
            if win_judge==BLACK:
                p1_win+=1
                break
            elif win_judge==WHITE:
                p2_win+=1
                break
            elif win_judge==3:
                draw+=1
                break

            #後手のターン
            env.p2_turn()

            #盤面の描画
            env.display_screen()

            #勝敗判定
            win_judge = env.winner() 

            #勝敗判定
            if win_judge==BLACK:
                p1_win+=1
                break
            elif win_judge==WHITE:
                p2_win+=1
                break
            elif win_judge==3:
                draw+=1
                break
        env = None
    print('先手勝利回数:', p1_win)
    print('後手勝利回数:', p2_win)
