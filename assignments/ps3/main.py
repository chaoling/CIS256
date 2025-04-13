'''
Name : sudoku.py
Author  : FirstName LastName
Version : 1.0
Description : A Sudoku Solver
'''
import csv
import argparse
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
        #check row:
        row,col = coord
        #find which box the number belong:
        r = row//3*3
        c = col//3*3
        if number in self.board[row]:
            return False
        elif number in [self.board[i][col] for i in range(9) ]: #check column
            return False
        elif number in [self.board[i][j] for i in range(r,r+3) for j in range(c,c+3)]: #check box
            return False
        return True

    def solve(self):
        #let's solve it using back tracking, like in the maze,
        #we also call it the depth first search
        for row in range(9):
            for col in range(9):
                if not self.board[row][col]: #only work when there is empty slot to solve
                    for num in range(1,10):
                        if self.isAllowed(num, (row, col)):
                           self.board[row][col] = num
                           if self.solve(): #solve a matrix of smaller problem
                               return True
                    else:
                        #if here, no solution found for that slot, back tracking
                        self.board[row][col] = 0 # clean the solt for next try
                        return False
        #when out of the outer loop, you've either found a solution or no solution found:
        return True

    def backtrack(self, i, j):
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
    #TODO: read the init board layout from a file
    '''
    init_board = [
        [4, 0, 0, 0, 0, 5, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 9, 8],
        [3, 0, 0, 0, 8, 2, 4, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 8, 0],
        [9, 0, 3, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 3, 0, 6, 7, 0],
        [0, 5, 0, 0, 0, 9, 0, 0, 0],
        [0, 0, 0, 2, 0, 0, 9, 0, 7],
        [6, 4, 0, 3, 0, 0, 0, 0, 0],
    ]
    '''
    sodoku = Sudoku(init_board)
    if sodoku.solve():
    #if sodoku.backtrack(0,0):
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
    