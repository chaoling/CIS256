'''
Name : sudoku.py
Author  : Dylan McCoy
Version : 1.0
Description : A Sudoku Solver
'''

import csv
import argparse
from typing import List

class Sudoku:
    def __init__(self, board):
        self.board = board
        self.print_soduko()
        self.M = len(board) #num of rows
        self.N = len(board[0]) #num of cols

    def isAllowed(self, number, coord):
        row, col = coord

        #check if number is already in row
        if number in self.board[row]:
            return False #number was in row already, move not allowed

        #check if number is already in col
        if number in [self.board[i][col] for i in range(9)]:
            return False #number was found in col already, move not allowed

        #determine top left most corner of subgrid using professor's approach
        r = (row // 3) * 3
        c = (col // 3) * 3

        #check if number is in subgrid using professor's approach
        if number in [self.board[i][j] for i in range(r, r + 3) for j in range(c, c + 3)]:
            return False #number was found in subgrid already, move not allowed

        return True #number not found yet, so it can go in this position

    def solve(self):
        for row in range(self.M):
            for col in range(self.N):
                if not self.board[row][col]: #looks for empty cell
                    for num in range(1, 10): #tries all numbers 1 through 9
                        if self.isAllowed(num, (row, col)):
                            self.board[row][col] = num #places the number in the spot
                            if self.solve(): #solves the remaining unfilled cells
                                return True
                    else:
                        self.board[row][col] = 0 #backtrack using professor's approach
                        return False #no valid number was found, puzzle wasn't solved
        return True #no more empty cells, puzzle has been solved

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
    sudoku = Sudoku(init_board)
    #if sodoku.backtrack(0,0):
    if sudoku.solve():
        sudoku.print_soduko()
    else:
        print("No solution found for this problem!!!")

def loadBoard(csvPath: str) -> List[List]:
    board = [[0 for _ in range(9)] for _ in range(9)]
    try:
        with open(csvPath, 'r') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                for j, item in enumerate(row):
                    board[i][j] = int(item)
        return board
    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process command-line arguments')
    parser.add_argument('-p', '--path', default='board.csv',
                        help='Path to the CSV file containing the Sudoku board')
    args = parser.parse_args()
    board = loadBoard(args.path)
    main(board)