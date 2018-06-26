# -*- coding: utf-8 -*-
import os
import numpy as np
import random
import glob
import sys
import copy
#2018/06/19
#made by Kazunari Morita

class Gomokunarabe_tree:

    def __init__(self):
        self.name = os.path.splitext(os.path.basename(__file__))[0]
        self.Blank = 0
        self.White = 1
        self.Black = 2
        self.screen_n_rows = 15
        self.screen_n_cols = 15
        self.enable_actions = np.arange(self.screen_n_cols*self.screen_n_rows)
        self.screen = np.zeros((self.screen_n_rows, self.screen_n_cols))

    def reset(self):
        """ 盤面の初期化 """
        # reset ball position
        self.screen = np.zeros((self.screen_n_rows, self.screen_n_cols))

    #盤面評価関数
    def score(self):
        b_score = 0
        w_score = 0
        #横の判定
        for i in range(15):
            for j in range(11):
                b_counter=0
                w_counter=0
                bs_counter=0
                ws_counter=0
                for k in range(5):
                    if self.screen[i][j+k]==1:
                        #黒カウント
                        b_counter+=1
                        bs_counter+=1
                        w_counter=0
                        ws_counter=0
                    if self.screen[i][j+k]==2:
                        #白カウント
                        w_counter+=1
                        ws_counter+=1
                        b_counter=0
                        bs_counter=0
                    if self.screen[i][j+k]==0:
                        #空白検出
                        bs_counter+=1
                        ws_counter+=1
                if (bs_counter>=5 and b_counter > 0):#黒スコア加算
                    b_score += pow(10, b_counter)
                if (ws_counter>=5 and w_counter > 0):#白スコア加算
                    w_score += pow(10, w_counter)
        
        #縦の判定
        for i in range(15):
            for j in range(11):
                b_counter=0
                w_counter=0
                bs_counter=0
                ws_counter=0
                for k in range(5):
                    if self.screen[j+k][i]==1:
                        #黒カウント
                        b_counter+=1
                        bs_counter+=1
                        w_counter=0
                        ws_counter=0
                    if self.screen[j+k][i]==2:
                        #白カウント
                        w_counter+=1
                        ws_counter+=1
                        b_counter=0
                        bs_counter=0
                    if self.screen[j+k][i]==0:
                        #空白検出
                        bs_counter+=1
                        ws_counter+=1
                if (bs_counter>=5 and b_counter > 0):#黒スコア加算
                    b_score += pow(10, b_counter)
                if (ws_counter>=5 and w_counter > 0):#白スコア加算
                    w_score += pow(10, w_counter)

        #斜め(右下)の判定
        for i in range(11):
            for j in range(11):
                b_counter=0
                w_counter=0
                bs_counter=0
                ws_counter=0
                for k in range(5):
                    if self.screen[i+k][j+k]==1:
                        #黒カウント
                        b_counter+=1
                        bs_counter+=1
                        w_counter=0
                        ws_counter=0
                    if self.screen[i+k][j+k]==2:
                        #白カウント
                        w_counter+=1
                        ws_counter+=1
                        b_counter=0
                        bs_counter=0
                    if self.screen[i+k][j+k]==0:
                        #空白検出
                        bs_counter+=1
                        ws_counter+=1
                if (bs_counter>=5 and b_counter > 0):#黒スコア加算
                    b_score += pow(10, b_counter)
                if (ws_counter>=5 and w_counter > 0):#白スコア加算
                    w_score += pow(10, w_counter)

        #斜め(左下)の判定    
        for i in range(11):
            for j in range(4,15):
                b_counter=0
                w_counter=0
                bs_counter=0
                ws_counter=0
                for k in range(5):
                    if self.screen[i+k][j-k]==1:
                        #黒カウント
                        b_counter+=1
                        bs_counter+=1
                        w_counter=0
                        ws_counter=0
                    if self.screen[i+k][j-k]==2:
                        #白カウント
                        w_counter+=1
                        ws_counter+=1
                        b_counter=0
                        bs_counter=0
                    if self.screen[i+k][j-k]==0:
                        #空白検出
                        bs_counter+=1
                        ws_counter+=1
                if (bs_counter>=5 and b_counter > 0):#黒スコア加算
                    b_score += pow(10, b_counter)
                if (ws_counter>=5 and w_counter > 0):#白スコア加算
                    w_score += pow(10, w_counter)
        
        #print ('\n\n')
        #print ('score:',b_score-w_score)
        #print ('\n\n')
        return b_score-w_score


    #勝った方のラベル返す(いたら)
    def winner(self):
        #横の判定  
        for i in range(15):
            p_judge=0
            e_judge=0        
            for j in range(15):
                if self.screen[i][j]==1:
                    p_judge+=1
                    e_judge=0
                if self.screen[i][j]==2:
                    e_judge+=1
                    p_judge=0
                if self.screen[i][j]==0:
                    #もし, 連続していなかったら0
                    p_judge=0
                    e_judge=0
                if p_judge>=5:
                    #盤面の描画
                    # self.display_screen()
                    print ('\n\n')
                    print ('You Win a')
                    print ('\n\n')
                    return 1
                
                if e_judge>=5:
                    #盤面の描画
                    # self.display_screen()
                    
                    print('\n\n')
                    print('You Lose a')
                    print('\n\n')
                    return 2


        #縦の判定
        for i in range(15):
            p_judge=0
            e_judge=0
            for j in range(15):
                if self.screen[j][i]==1:
                    p_judge+=1
                    e_judge=0
                if self.screen[j][i]==2:
                    e_judge+=1
                    p_judge=0
                if self.screen[j][i]==0:
                    #もし, 連続していなかったら0
                    p_judge=0
                    e_judge=0
        
                if p_judge>=5:
                    #盤面の描画
                    # self.display_screen()
                    
                    print ('\n\n')                    
                    print ('You Win b')
                    print ('\n\n')
                    return 1
                
                if e_judge>=5:
                    #盤面の描画
                    # self.display_screen()
                    print ('\n\n')
                    print ('You Lose b')
                    print ('\n\n')
                    return 2

        #斜め(右下)の判定
        for i in range(11):
            for j in range(11):
                p_judge=0
                e_judge=0
                for k in range(5):
                    if self.screen[i+k][j+k]==1:
                        p_judge+=1
                        e_judge=0
                    if self.screen[i+k][j+k]==2:
                        e_judge+=1
                        p_judge=0

                    if self.screen[i+k][j+k]==0:
                        #もし, 連続していなかったら0
                        p_judge=0
                        e_judge=0

                    if p_judge>=5:
                        #盤面の描画
                        # self.display_screen()
                    
                        print ('You Win c')
                        print ('\n\n')
                        return 1
                    
                    if e_judge>=5:
                        #盤面の描画
                        # self.display_screen()
                    
                        print ('\n\n')                        
                        print ('You Lose c')
                        print ('\n\n')
                        return 2

        #斜め(左下)の判定    
        for i in range(11):
            for j in range(4,15):
                p_judge=0
                e_judge=0
                for k in range(5):
                    if self.screen[i+k][j-k]==1:
                        p_judge+=1
                        e_judge=0
                    if self.screen[i+k][j-k]==2:
                        e_judge+=1
                        p_judge=0
                    if self.screen[i+k][j-k]==0:
                        #もし, 連続していなかったら0
                        p_judge=0
                        e_judge=0

                    if p_judge>=5:
                        #盤面の描画
                        # self.display_screen()
                    
                        print ('You Win d')
                        print ('\n\n')
                        return 1
                    
                    if e_judge>=5:
                        #盤面の描画
                        # self.display_screen()
                    
                        print ('You Lose d')
                        print ('')
                        return 2

        #引き分け判定
        if 0 not in self.screen:
            #盤面の描画
            # self.display_screen()
                    
            print ('Draw')
            print ('\n\n')
            return 0

        return False



        

    def get_cells(self, i):
        r = int(i / self.screen_n_cols)
        c = int(i - ( r * self.screen_n_cols))
        return self.screen[r][c]  


    def get_enables(self,color):
        result = []
        #おける座標のリストを返す
        for action in self.enable_actions:
            if self.get_cells(action) == 0:
                """ 空白の位置 """
                result.insert(0,action)

        return result



    def update(self, action, color):

        pos_y = int(action / self.screen_n_cols)
        pos_x = int(action-( pos_y * self.screen_n_cols))
        self.screen[pos_y][pos_x] = color


        # print(self.screen)
        n =  self.count_my_ball(color,action)
        return n


    def count_my_ball(self,color,action):
        pos_y = action//15    
        pos_x = action/15

        pos_y = int(action / self.screen_n_cols)
        pos_x = int(action-( pos_y * self.screen_n_cols))

   
        right_margin = pos_x-14
        left_margin = pos_x
        top_margin = pos_y
        under_margin = pos_y-14


        # print (min(right_margin,left_margin))
        # exit(-1)
        ball_num = [0]*6



        #右側
        if right_margin>5:
            for i in range(5):
                if self.screen[pos_x+i][pos_y]==color:
                    ball_num[0]+=1
                else:
                    ball_num[0]-=1

        else:
            for i in range(right_margin):
                if self.screen[pos_x+i][pos_y]==color:
                    ball_num[0]+=1
                else:
                    ball_num[0]-=1                
        
        #下側
        if under_margin>5:
            for i in range(5):
                if self.screen[pos_x][pos_y+i]==color:
                    ball_num[1]+=1
                else:
                    ball_num[1]-=1    
        else:
            for i in range(under_margin):
                if self.screen[pos_x][pos_y+i]==color:
                    ball_num[1]+=1
                else:
                    ball_num[1]-=1       
        #左側
        if left_margin>5:
            for i in range(5):
                if self.screen[pos_x-i][pos_y]==color:
                    ball_num[2]+=1
                else:
                    ball_num[2]-=1
        else:
            for i in range(left_margin):
                if self.screen[pos_x-i][pos_y]==color:
                    ball_num[2]+=1
                else:
                    ball_num[2]-=1        
        #上側
        if top_margin>5:
            for i in range(5):
                if self.screen[pos_x][pos_y-i]==color:
                    ball_num[3]+=1
                else:
                    ball_num[3]-=1
        else:
            for i in range(top_margin):
                if self.screen[pos_x][pos_y-i]==color:
                    ball_num[3]+=1
                else:
                    ball_num[3]-=1
        #右斜上側
        if right_margin>5 and top_margin>5:
            for i in range(5):
                if self.screen[pos_x+i][pos_y+i]==color:
                    ball_num[4]+=1
                else:
                    ball_num[4]-=1
        else:
            for i in range(min(right_margin,top_margin)):
                if self.screen[pos_x+i][pos_y+i]==color:
                    ball_num[4]+=1
                else:
                    ball_num[4]-=1    
        #左斜上側
        if left_margin>5 and top_margin>5:
            for i in range(5):
                if self.screen[pos_x-i][pos_y-i]==color:
                    ball_num[5]+=1
                else:
                    ball_num[5]-=1
        else:
            for i in range(min(left_margin,top_margin)):
                if self.screen[pos_x-i][pos_y-i]==color:
                    ball_num[5]+=1
                else:
                    ball_num[5]-=1        
        #左斜下側
        if left_margin>5 and under_margin>5:
            for i in range(5):
                if self.screen[pos_x-i][pos_y+i]==color:
                    ball_num[6]+=1
                else:
                    ball_num[6]-=1
        else:
            for i in range(min(left_margin,under_margin)):
                if self.screen[pos_x-i][pos_y+i]==color:
                    ball_num[6]+=1
                else:
                    ball_num[6]-=1        
        #右斜下側
        if right_margin>5 and under_margin>5:
            for i in range(5):
                if self.screen[pos_x+i][pos_y+i]==color:
                    ball_num[7]+=1
                else:
                    ball_num[7]-=1
        else:
            for i in range(min(right_margin,under_margin)):
                if self.screen[pos_x+i][pos_y+i]==color:
                    ball_num[7]+=1
                else:
                    ball_num[7]-=1


        # print (str(right_margin))
        # print (left_margin))
        # print (top_margin))
        # # print (under_margin))
        # print ('玉数:'+str(max(ball_num)))
        # print (str(color))
        # print (max(ball_num))
        return max(ball_num)
    
    def isEnd(self):
        # e1 = self.get_enables(self.White)
        # e2 = self.get_enables(self.Black)

        # self.winner()
            # return True

        # for action in self.enable_actions:
            # if self.get_cells(action) == self.Blank:
        # self.display_screen()
        return self.winner() 
        
        # return True    

    #プレイヤーのターン
    def player_turn(self):
        print ('Your Turn')
        
        value, i, j = self.search_AI(2, 1)

        p_x_pos = i
        p_y_pos = j
        #p_x_pos = input('select ball x pos > ')
        #p_y_pos = input('select ball y pos > ')

        if int(p_x_pos) == 0:
            return 0
        while self.screen[int(p_y_pos)-1][int(p_x_pos)-1] == 1 or  self.screen[int(p_y_pos)-1][int(p_x_pos)-1] == 2 or int(p_x_pos)<1 or int(p_x_pos)>15 or  int(p_y_pos)<1 or int(p_y_pos)>15: 

            print ('please retry')
            p_x_pos = input('select ball x pos > ')
            p_y_pos = input('select ball y pos > ')
        self.screen[int(p_y_pos)-1][int(p_x_pos)-1] = 1

    #敵のターン
    def enemy_turn(self):
        print ('Enemy Turn')

        value, i, j = self.search_AI(1, 1)

        p_x_pos = i
        p_y_pos = j
        if int(p_x_pos) == 0:
            return 0
        while self.screen[int(p_y_pos)-1][int(p_x_pos)-1] == 1 or  self.screen[int(p_y_pos)-1][int(p_x_pos)-1] == 2 or int(p_x_pos)<1 or int(p_x_pos)>15 or  int(p_y_pos)<1 or int(p_y_pos)>15: 

            print ('please retry')
            p_x_pos = input('select ball x pos > ')
            p_y_pos = input('select ball y pos > ')
        self.screen[int(p_y_pos)-1][int(p_x_pos)-1] = 2

    #AI
    def search_AI(self, turn ,depth):
        if depth == 0:
            return self.score(), 0, 0
        
        if turn == 1:
            value = -100000
            v = -100000
        else:
            value = 100000
            v = 100000
        move = [0,0]
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
                    b.screen[i][j] = turn
                    v = b.score()
                    #if abs(v) > 10000:
                    #    return v, j+1, i+1
                    if turn == 1:
                        v, a, b = b.search_AI(2, depth - 1)
                        if value < v:
                            value = v
                            move = [j+1,i+1]
                    else:
                        v, a, b = b.search_AI(1, depth - 1)
                        if value > v:
                            value = v
                            move = [j+1,i+1]
        if start_flag == 1:
            return 0, 8, 8
        print(move, ':' ,value)
        b = None
        return value, move[0], move[1]
    
    #盤面の表示
    def display_screen(self):
        print ('    1 2 3 4 5 6 7 8 9 A B C D E F')
        for i in range(15):
            print(hex(i+1), end='')
            for j in range(15):
                # if i==0 and j==0:
                #     for k in range(1,16):
                #         print (str(k)+'　', end='')
                #     print ('\n',end='')
                if  self.screen[i][j]==0:
                    print ('  ', end='')

                elif self.screen[i][j]==1:
                    print ('〇', end='')

                elif self.screen[i][j]==2:
                    print ('✖', end='')

            print ('\n', end='')
            
        print ('[You]'+' 〇', '\t[Enemy]'+' ✖')
        print ('\n\n')

#メイン文
if __name__ == '__main__':

    env = Gomokunarabe_tree()

    end_flag = 0
    # screen = np.zeros([15,15])
    while end_flag ==0:

        #盤面の描画
        env.display_screen()

        #敵のターン
        env.enemy_turn()

        #勝敗判定
        end_flag = env.winner()

        #スコア表示
        env.score()
        
        #盤面の描画
        env.display_screen()

        #プレイヤーのターン
        env.player_turn()

        #勝敗判定
        end_flag = env.winner()

        #スコア表示
        env.score()