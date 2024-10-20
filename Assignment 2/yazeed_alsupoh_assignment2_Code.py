import re
import time

# Extract the items from the text file
file = open('Assignment 2 sudoku.txt', 'r')
items = file.readlines()

# Removing elements that are not part of the items array
del items[0:5]

N = 9
grids = []
for i in range(10):
    grids.append(items[i*11: (i*11)+9])


for grid in grids:
    for i in range(len(grid)):
        grid[i] = [int(x) for x in list(grid[i][0:9])]
 
def trueNum(grid, row, col, num):
    # Checking row and column:
    for x in range(9):
        if grid[row][x] == num or grid[x][col] == num:
            return False
        
    
    # Checking in the same 3x3 subgrid:
    startRow = row - row % 3
    startCol = col - col % 3

    for i in range(3):
        for j in range(3):
            if grid[i + startRow][j + startCol] == num:
                return False
    
    return True
 
def solveSudoku(grid, row, col):
    if (row == N - 1 and col == N):
        # PUZZLE IS SOLVED
        return True

    if col == N:
        # If we reached the last column
        # it moves to the next row 
        # and resets the column to 0.
        row += 1
        col = 0

    # if empty: 
    if grid[row][col] > 0:
        # the function moves to the next cell
        # by calling itself with column + 1
        return solveSudoku(grid, row, col + 1)
    # not empty
    else:
        # 1 to 9 (inclusive) with step 1
        for num in range(1, N + 1):
            if trueNum(grid, row, col, num):
                grid[row][col] = num
                if solveSudoku(grid, row, col + 1): # next cell
                    return True
            
            # if the puzzle cannot be solved with the current move,
            # the function backtracks by resetting the current cell to 0
            grid[row][col] = 0
    return False

def show(arr):
    for i in range(N):
        for j in range(N):
            print(arr[i][j], end = " ")
        print()
    print("*****SUDOKU******")
 
# Driver Code
start = time.time()
for suokdu in grids:
    solveSudoku(suokdu, 0, 0)
    show(suokdu)

end = time.time()
print("Execution Time: ", end-start)
