'''
Name : sudoku.py
Author  : Katie Inman
Version : 1.0
Description : A Sudoku Solver
'''
import csv
import argparse
from typing import List

#handles the solving of the Sudoku puzzle
class Sudoku:
    def __init__(self, board):
        #initialize the board and print it
        self.board = board
        self.print_soduko()
        self.M = len(board) #number of rows
        self.N = len(board[0]) #number of columns

    def isAllowed(self, number, coord):
        '''
        Checks if a number can be placed at the given coordinate
        '''

        row, col = coord
        r = row//3*3 #calculate starting row of the 3x3 box
        c = col//3*3 #calculate starting column of the 3x3 box
        
        #check if the number already exists in the row, column, or subgrid
        if number in self.board[row]:
            return False
        elif number in [self.board[i][col] for i in range(self.M)]:
            return False
        elif number in [self.board[r+i][c+j] for i in range(r, r+3) for j in range (c, c+3)]:
            return False
        else:
            return True

    def solve(self):
        '''
        Solves the Sudoku puzzle using backtracking
        '''
        for row in range(self.M):
            for col in range(self.N):
                if not self.board[row][col]: #find an empty cell
                    for number in range(1, self.M+1):
                        if self.isAllowed(number, (row, col)): #Check if number can be placed
                            self.board[row][col] = number
                            if self.solve(): #recursively try to solve
                                return True
                    else:
                        self.board[row][col] = 0 #backtrack is no solution
                        return False
        
        return True  #puzzle solved  
        
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
        '''
        Prints the Sudoku board in a readable format
        '''
        print("+" + "---+"*9) #print the first row: +---+---+---+....
        for i, row in enumerate(self.board):
            print(("|" + " {} | {} | {} |"*3).format(*[x if x != 0 else " " for x in row]))
            if i % 3 == 2:
                print("+" + "===+"*9) #print separator after every 3 rows
            else:
                print("+" + "---+"*9)

def main(init_board):
    sodoku = Sudoku(init_board)
    #if sodoku.backtrack(0,0):
    if sodoku.solve(): #try to solve using backtracking
        sodoku.print_soduko() #print solved board
    else:
        print("No solution found for this problem!!!")

def loadBoard(csvPath: str) -> List[List]:
    '''
    Load a CSV file containing board data into a container
    @param csvPath the path to the CSV file
    @return a container holding the suduko board
    '''
    board =[[0 for _ in range(9)] for _ in range(9)] #initialize an empty 9x9 board
    try:
        with open(csvPath,'r') as file:
            reader = csv.reader(file)
            for i,row in enumerate(reader):
                for j, item in enumerate(row):
                    board[i][j] = int(item) #convert CSV string to integers

        return board
    except Exception as ex:
        print(ex) #error handling



if __name__ == "__main__":
    #command-line argument parser
    parser = argparse.ArgumentParser(description='Process cmd line arguments')
    parser.add_argument('-p','--path', default='board.csv',
                    help='path to the csv file')

    args = parser.parse_args()
    board = loadBoard(args.path) #load board from provided CSV path
    main(board) #solve the puzzle