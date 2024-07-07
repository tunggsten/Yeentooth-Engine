import pygame
from tkinter import *

# Mathmatical Objects
class matrix:
    def __init__(self, contents: list):
        self.contents = contents # This assumes you're smart and don't need input validation. 
        
                                 # I'm potentially going to be making a lot of new matrices 
                                 # in the main loop, so I'd rather not spend four years running
                                 # nine million conditionals every single frame to make sure I 
                                 # haven't messed the parameters up. 
                                 
                                 # I'll regret this later but we'll burn that bridge when we 
                                 # come to it.
                                 
        self.order = (len(contents), len(contents[0])) # Number of rows followed by the number of collumbs
        
    def get_contents(self):
        return self.contents
    
    def set_contents(self, contents):
        self.contents = contents
        self.order = (len(contents), len(contents[0])) # Same as in __init__()
        
    def multiply_contents(self, coefficient): # If you need to divide a matrix, you can just multiply it by the reciprocal of your coefficient.        
                                              # Like this: matrix.multiply_contents(1 / numberYoureDividingBy)
        multiplied = []
        
        for i in range(self.order[0]):
            multiplied.append([])
            
            for j in range(self.order[1]):
                multiplied[i].append(self.contents[i][j] * coefficient)
        
    def get_order(self):
        return self.order
        
    def get_transpose(self): # This swaps the rows and collumbs. It's like reflecting the matrix diagonally.
        transpose = []
        
        for i in range(self.order[1]):
            row = []
            
            for j in range(self.order[0]):
                row.append(self.contents[j][i])
            transpose.append(row)
        
        return matrix(transpose)
    
    def get_2x2_determinant(self): # Okay, I know this is really ugly but you can only 
                                   # find determinants for square matrices, and I'm only gonna be
                                   # doing that for 2x2 and 3x3 ones so I might as well reduce the
                                   # conditionals.
        return (self.contents[0][0] * self.contents[1][1]) - (self.contents[0][1] * self.contents[1][0])
    
    def get_2x2_inverse(self):
        det = self.get_2x2_determinant()
        
        inverse = [
            [self.contents[1][1], -self.contents[0][1]],
            [-self.contents[1][0], self.contents[0][0]]
        ]
        
        try:
            return matrix(inverse).multiply_contents(1 / det)
        except:
            print(f"The matrix {self} is singular, so it has no inverse")
            return None
    
    def get_3x3_determinant(self): # This is based on the Rule of Saurus
        return (
                (self.contents[0][0] * self.contents[1][1] * self.contents[2][2]) +
                (self.contents[0][1] * self.contents[1][2] * self.contents[2][0]) +
                (self.contents[0][2] * self.contents[1][0] * self.contents[2][1]) -
                
                (self.contents[2][0] * self.contents[1][1] * self.contents[0][2]) -
                (self.contents[2][1] * self.contents[1][2] * self.contents[0][0]) -
                (self.contents[2][2] * self.contents[1][0] * self.contents[0][1])
               )
        
    def get_3x3_inverse(self):
        # This is a long-winded confusing process which I hate.

        # Here's what we need to do:
        
        # Step 1: Find the determinant.
        det = self.get_3x3_determinant()
        
        # That wasn't so hard!
        
        # Step 2: Make a 3x3 matrix of minors:
        contents = self.get_contents()
        
        minors = matrix(
            [
                [
                    matrix([[ contents[1][1], contents[1][2] ], [ contents[2][1], contents[2][2] ]]).get_2x2_determinant(), 
                    matrix([[ contents[1][0], contents[1][2] ], [ contents[2][0], contents[2][2] ]]).get_2x2_determinant(), 
                    matrix([[ contents[1][0], contents[1][1] ], [ contents[2][0], contents[2][1] ]]).get_2x2_determinant()
                ],
                
                [
                    matrix([[ contents[0][1], contents[0][2] ], [ contents[2][1], contents[2][2] ]]).get_2x2_determinant(), 
                    matrix([[ contents[0][0], contents[0][2] ], [ contents[2][0], contents[2][2] ]]).get_2x2_determinant(), 
                    matrix([[ contents[0][0], contents[0][1] ], [ contents[2][0], contents[2][1] ]]).get_2x2_determinant()
                ],
                
                [
                    matrix([[ contents[0][1], contents[0][2] ], [ contents[1][1], contents[1][2] ]]).get_2x2_determinant(), 
                    matrix([[ contents[0][0], contents[0][2] ], [ contents[1][0], contents[1][2] ]]).get_2x2_determinant(), 
                    matrix([[ contents[0][0], contents[0][1] ], [ contents[1][0], contents[1][1] ]]).get_2x2_determinant()
                ]
            ]
        )
        
        # This makes me want to kill myself.
        
        # Basically, we're making a 2x2 matrix out of all the elements that 
        # *aren't in the same row or collumb* as the element we're finding a minor for.
        # Then, the minor is just the determinant of that 2x2 matrix.
        
        # Example:
        
        
        
         
                

# Graphics Objects
class vertex:
    def __init__(self, position):
        self.position = matrix(position).get_transpose() # Stores the vertex's position as a collumb vector
    
    def get_position(self):
        return self.position
    
    def set_position(self, position):
        self.position = position
        
    def translate_by(self, vector):
        self.position += vector
        
    def rotate_euler()
        
testMatrix = matrix([[1, 4, -4], [2, 9, 3]])
print(testMatrix.get_order())
print(testMatrix.get_transpose().get_contents())

test3x3matrix = matrix([[3, 1, 0], [0, -9, 2], [-1, -4, 1]])
print(test3x3matrix.get_3x3_determinant())
print(test3x3matrix.get_transpose().get_contents())

test2x2matrix = matrix([[1, 0], [0, -1]])
print(test2x2matrix.get_2x2_inverse().get_contents())

# Pygame Setup - initialises the window, 
pygame.init()
window = pygame.display.set_mode((320, 240))
clock = pygame.time.Clock()
running = True