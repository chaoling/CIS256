'''
Name : sudoku.py
Author  : Kristi Ogden
Version : 1.0
Description : A Sudoku Solver

----psuedocode----
Create state checker, can a number exist in a cell (no match in row, col, box)
DFS over every row and column to check if a number can exist in that cell if it is equal to 0
if it is, go to next cell
if it is not, reset cell and try with next number

repeat for every cell


----reflection---
One of the biggest hurdles was getting the recursion and indentation levels right. I had the right code for several
iterations but one of the checks was one to few indentations in and it hit recursion deptch limit
this was a massive exercise is understanding recursion better because I do not frequently work with it iin my own
paraprofessional space as most data is flat
'''
import csv
import argparse
import math
from typing import List

#Let's start with a simple sudoku solver:
#basic rules: 9x9 matrix, unique numbers (1-9) in each row, col and 3x3 sub-matrix
class Sudoku:
    def __init__(self, board):
        self.board = board
        self.print_soduko()
        self.M = len(board) #num of rows
        self.N = len(board[0]) #num of cols

    def isAllowed(self, number, coord):
        #FIXME(1)
        '''
        Given a number and coord (row,col), return if this number is allowe in sudoku
        '''
        pass
        #get row,col = coord

        #find which box the number belong:

        #check row

        #check col

        #check box

        for i in range(0, self.N):
            if self.board[coord[0]][i] == number:
                return False
        for i in range(0, self.N):
            if self.board[i][coord[1]] == number:
                return False
        box = int(math.sqrt(self.N))
        x_box_0 = (coord[1] // box) * box
        y_box_0 = (coord[0] // box) * box
        for i in range(0, box):
            for j in range(0, box):
                if self.board[y_box_0 + i][x_box_0 + j] == number:
                    return False
        return True

    def solve(self):
        #FIXME: (2)
        '''
        recursively explore each number in the empty slot and backtrack if dead end reached
        if find one solution, return
        else return False, aka, no solution.
        '''
        #let's solve it using back tracking, like in the maze,
        #we also call it the depth first search
        #iterate each row and col: (double loop)
             #try test all possible number in that row and col if self.board[row][col] is empty.
                #if one of the num is allowed there (using the allowed function)
                #recursively call the solve() with the new move
                    #if solve() returns true:
                        #return True

             #else:
                #if here, no solution found for that slot, back tracking
                # clean the solt for next try
                # return False since all else failed

        #when out of the outer loop, you've either found a solution or no solution found:
        #return True

        for row in range(self.N):
            for col in range(self.N):
                if self.board[row][col] == 0:
                    for n in range(1, self.N):
                        if self.isAllowed(n, (row, col)):
                            self.board[row][col] = n
                            if not self.solve():
                                self.board[row][col] = 0
                                return False
                    return False
        return True

    def backtrack(self, i, j):
        '''
        you can use this function to check the answer (replace self.solve() with self.backtrack(...))
        it provides another point of view for backtracking recursively
        '''
        if j == self.N: #continue with next row if col is out of boundary
            return self.backtrack(i+1,0)
        if i == self.M: #found one solution, return base case
            return True
        if self.board[i][j] != 0:
            #skip it, this is the location that has pre-defined numbers
            return self.backtrack(i, j+1)
        for num in range(1,10):
            if not self.isAllowed(num, (i,j)):
                continue
            self.board[i][j] = num
            if self.backtrack(i, j+1):
                return True
            self.board[i][j] = 0
        return False #can't find the solution with 1-9


    def print_soduko(self):
        print("+" + "---+"*9) #print the first row: +---+---+---+....
        for i, row in enumerate(self.board):
            print(("|" + " {} | {} | {} |"*3).format(*[x if x != 0 else " " for x in row]))
            if i % 3 == 2:
                print("+" + "===+"*9)
            else:
                print("+" + "---+"*9)

def main(init_board):
    sodoku = Sudoku(init_board)
    #if sodoku.backtrack(0,0):
    if sodoku.solve():
        sodoku.print_soduko()
    else:
        print("No solution found for this problem!!!")

def loadBoard(csvPath: str) -> List[List]:
    '''
    Load a CSV file containing board data into a container
    @param csvPath the path to the CSV file
    @return a container holding the suduko board
    '''
    board =[[0 for _ in range(9)] for _ in range(9)] #note caveat: don't do this-> [[0]*9]*9 why? (hint: aliasing)
    try:
        with open(csvPath,'r') as file:
            reader = csv.reader(file)
            for i,row in enumerate(reader):
                for j, item in enumerate(row):
                    board[i][j] = int(item)

        return board
    except Exception as ex:
        print(ex)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process cmd line arguments')
    parser.add_argument('-p','--path', default='board.csv',
                    help='path to the csv file')

    args = parser.parse_args()
    board = loadBoard(args.path)
    main(board)