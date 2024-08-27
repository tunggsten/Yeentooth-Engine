import pygame
from tkinter import *

import math
import random
import time



# ---------------- MATHEMATICAL OBJECTS ----------------

class Matrix:  
    def __init__(self, contents: list[list[float]]): # All the functions in this class are slower than my 
                                                     # grandma's metabolism and she's dead.
                                                     
                                                     # Unfortunately for the poor souls who have to mark
                                                     # and moderate this, I will not be using Numpy instead
                                                     # bc that's not enough work!! And who needs GPU 
                                                     # acceleration in their game engine anyway? 
                                        
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
       
    def set_contents(self, contents: list[list[float]]):
        self.contents = contents
        self.order = (len(contents), len(contents[0])) # Same as in __init__()
         
    def multiply_contents(self, coefficient: float): # If you need to divide a matrix, you can just multiply 
                                                     # it by the reciprocal of your coefficient.        
                                                     # Like this: Matrix.multiply_contents(1 / numberYoureDividingBy)
        multiplied = []
        
        for i in range(self.order[0]):
            multiplied.append([])
            
            for j in range(self.order[1]):
                multiplied[i].append(self.contents[i][j] * coefficient)
                
        return Matrix(multiplied)
         
    def get_order(self):
        return self.order
         
    def get_transpose(self): # This swaps the rows and collumbs. It's like reflecting the matrix diagonally.
        transpose = []
        
        for i in range(self.order[1]):
            row = []
            
            for j in range(self.order[0]):
                row.append(self.contents[j][i])
            transpose.append(row)
        
        return Matrix(transpose)
     
    def get_2x2_determinant(self): # I know this is really ugly but you can only find 
                                   # determinants for square matrices, and I'm only gonna be
                                   # doing that for 2x2 and 3x3 ones so I might as well reduce the
                                   # conditionals and make order-specific functions.
        return (self.contents[0][0] * self.contents[1][1]) - (self.contents[0][1] * self.contents[1][0])
    
    def get_2x2_inverse(self): # This just uses the set formula.
        
                               # [ [ a, b ],           =  1 / Det  *  [ [ d, -b ],
                               #   [ c, d ] ] ^ -1                      [ -c, a ] ]
        det = self.get_2x2_determinant()
        
        inverse = [
            [self.contents[1][1], -self.contents[0][1]],
            [-self.contents[1][0], self.contents[0][0]]
        ]
        
        try:
            return Matrix(inverse).multiply_contents(1 / det)
        except:
            print(f"The matrix {self} is probably singular, so it has no inverse")
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
        
        workingContents = [
                [
                    Matrix([[ self.contents[1][1], self.contents[1][2] ], [ self.contents[2][1], self.contents[2][2] ]]).get_2x2_determinant(), 
                    Matrix([[ self.contents[1][0], self.contents[1][2] ], [ self.contents[2][0], self.contents[2][2] ]]).get_2x2_determinant(), 
                    Matrix([[ self.contents[1][0], self.contents[1][1] ], [ self.contents[2][0], self.contents[2][1] ]]).get_2x2_determinant()
                ],
                
                [
                    Matrix([[ self.contents[0][1], self.contents[0][2] ], [ self.contents[2][1], self.contents[2][2] ]]).get_2x2_determinant(), 
                    Matrix([[ self.contents[0][0], self.contents[0][2] ], [ self.contents[2][0], self.contents[2][2] ]]).get_2x2_determinant(), 
                    Matrix([[ self.contents[0][0], self.contents[0][1] ], [ self.contents[2][0], self.contents[2][1] ]]).get_2x2_determinant()
                ],
                
                [
                    Matrix([[ self.contents[0][1], self.contents[0][2] ], [ self.contents[1][1], self.contents[1][2] ]]).get_2x2_determinant(), 
                    Matrix([[ self.contents[0][0], self.contents[0][2] ], [ self.contents[1][0], self.contents[1][2] ]]).get_2x2_determinant(), 
                    Matrix([[ self.contents[0][0], self.contents[0][1] ], [ self.contents[1][0], self.contents[1][1] ]]).get_2x2_determinant()
                ]
            ]
        
        # That was so hard!
        
        # Basically, for each minor we're making a 2x2 matrix out of all the elements that 
        # *aren't in the same row or collumb* as the element we're finding a minor for.
        # Then, the minor is just the determinant of that 2x2 matrix.
        
        # Example:
        
        #  [ [ 1, 6, 7 ],         Here, the minor of 1 (in the top left)
        #    [ 0, 4, 9 ],         is:
        #    [ 2, 3, 4 ] ]
        #                         Det([ [ 4, 9 ],
        #                               [ 3, 4 ] ] )
        #
        #                         which equates to 16 - 27, which is -11.
        
        # Uh oh! Looks like someone overheard us talking about minors!
        
        # ⠀⠀⠀⠀⠀⢀⠀⡀⠠⠀⠠⠀⠠⢀⠀⢔⠄⢀⢨⢣⠝⡬⡩⢝⠬⡣⡱⡱⡁⠀⢐⠅⠀⠀⠀⡀⢐⠪⣿⡯⣿⡯⣹⣿⣿⣿⣿⡿⣿⣿
        # ⠀⠀⠀⠀⠂⠠⠀⡀⠂⠠⠁⡈⢀⠂⠄⢰⡁⢄⠢⢃⠘⠔⠈⠂⡈⠐⠡⢊⠆⠢⡨⡃⠠⢀⠄⠠⠈⡂⠛⢁⠛⠃⢚⠋⠛⠛⠋⡑⠛⠛
        # ⠀⠀⠀⠀⠂⠀⠂⢀⠐⠀⠄⠠⢀⠂⠘⠀⠊⠀⠀⠀⢀⠀⠈⠀⠀⠀⠂⠀⠈⠀⠂⠈⠂⠁⠠⠁⠂⢄⠁⠄⠀⡁⢀⠈⢀⠁⠂⠀⠂⠠
        # ⠀⠀⠀⠠⠀⠁⠠⢀⠀⡂⠐⠠⠀⠀⠁⠀⠀⠀⠐⠀⠀⡀⠀⠀⠐⠀⡀⠀⠁⠐⠄⠈⠀⠀⠂⠈⠀⠀⠂⠂⠄⠀⠀⠀⠀⠀⠀⠁⠐⠀
        # ⠀⠀⠀⠀⠄⢈⠀⠄⠠⢀⠁⡀⠀⡀⠠⠀⠀⠄⠀⠀⠐⠀⠀⠀⠂⠠⠀⠀⠀⠀⠀⠀⠌⠐⠀⠐⠀⡈⠄⠈⠈⡀⠂⠁⠀⠁⠀⠂⠀⠀
        # ⠀⠀⠀⠐⠀⠄⠀⠄⠁⠐⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠈⢀⠀⡁⠐⠀⠀⢁⠈⠀⡀⠠⠀⠠⠀⠠⠈⢀⠀⠄⠐⢀⠀⠁⠀⠠⠀⠈
        # ⠀⠀⠀⠀⠄⠀⠂⠀⠂⠐⠀⠠⠀⢀⠀⠀⠀⠀⠀⠠⠀⠈⢀⠀⠀⠄⠀⠀⠂⢀⠐⠀⠀⠀⠀⠂⠈⠀⠂⠠⠀⡈⠂⠀⠄⠈⠀⢀⠀⠐
        # ⠀⠀⠀⢀⠀⠂⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠄⢁⠠⠀⠌⠠⡈⡀⠂⢄⠡⡈⢀⠂⢄⢁⠀⠂⢀⠁⠠⠀⡈⠂⠠⠀⢀⠀⠀⡀
        # ⠀⠀⠀⢀⠀⠄⠠⢀⠀⠀⠀⠀⠂⠀⠀⠀⠀⠂⠐⠀⢂⠐⢌⢂⠕⡨⢢⡈⢆⠐⡅⡢⠨⡢⡃⢔⢀⠁⠀⠠⠀⠠⠀⡈⠀⠂⠀⠀⠀⠀
        # ⠠⠀⢀⠀⠀⠀⡀⠀⠀⠀⠠⠀⠀⡀⠀⠁⢀⠀⢁⢘⢄⠣⡌⢎⡪⡘⡤⡫⡲⣡⢊⡆⠱⢜⢄⠹⡐⢬⡀⡑⢀⠁⡐⠀⠈⠀⠀⠀⠂⠀
        # ⠀⠀⠀⠀⠐⠐⠀⠀⠄⠀⠀⠀⠄⠀⠄⠀⡀⠀⡢⡑⢅⠣⠊⡡⠉⠚⠢⡫⣮⢣⡧⣹⢌⣦⡱⣕⡼⣢⢬⡀⠂⠌⠀⠀⠀⠀⠂⠀⠠⠀
        # ⠈⠀⠈⠀⠀⡀⠐⠀⠀⠀⢈⠀⠄⠀⡀⠀⢄⠔⡕⡑⡢⡲⡱⣕⢟⠳⡦⣰⣀⢛⣺⡳⣟⢮⣟⡮⡻⠑⢃⠂⠀⠄⠠⠀⠁⠀⠀⠄⠀⠀
        # ⠄⠀⠀⠂⢀⠀⠀⡀⠀⠂⠀⡠⢀⠀⠀⢀⠆⡣⢪⠸⡜⡪⠪⡠⡈⡨⣶⡰⣕⢝⢼⣝⣽⡳⡝⠔⣔⠫⡞⠂⠀⢀⠀⠀⠀⠠⠀⠀⠀⠀
        # ⠈⡈⢈⠂⠡⠀⠀⠀⠀⡢⣐⠑⠴⡡⠈⡢⡑⢕⢅⢏⢮⣫⣚⢖⡼⡲⣕⢷⡺⣌⢮⡺⣵⣝⣪⣂⢼⢃⡌⠀⠀⠀⠀⠈⠀⠀⠀⠀⠂⠀
        # ⠀⠀⠀⠀⠀⠀⠂⠀⠀⠘⡌⡮⣘⢆⠐⢌⠪⡒⣕⢕⢗⡼⣪⡻⣎⢿⣹⡵⡳⡜⡖⣽⡳⡮⡧⣯⣳⣝⠇⠀⠀⠁⠀⠀⠐⠀⠁⠀⠀⠠
        # ⠀⠀⠀⠀⠀⠀⡀⠀⠂⠀⠈⠺⠬⡢⡁⢪⢘⢜⢬⢣⢏⡾⡵⣯⡻⣵⡻⣞⢯⢚⢮⡪⣯⣻⢺⡞⣶⢝⡇⠀⠀⢀⠀⠁⠀⠀⠀⠠⠀⠀
        # ⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⡀⠀⠀⠨⡠⢑⢌⢖⢕⢧⡻⣜⡯⣾⣝⣯⡻⣵⡣⡳⡕⡝⣮⢟⡵⣿⣝⢯⡇⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀
        # ⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠄⠀⠐⢠⠑⡔⡕⡭⣺⢪⢷⣝⢾⢮⡳⣝⢮⡺⣕⣝⢮⡮⣳⢻⢮⣞⣯⠁⠀⠀⠂⠀⠈⠀⠀⠂⠀⠀⠁
        # ⠀⠀⠀⠀⠐⠈⠐⠀⠔⠀⠀⡀⠀⠈⡆⠱⡨⡪⣪⡣⣛⠶⣝⣯⡳⣍⠮⣳⣝⣮⣝⣳⣝⢕⢯⢷⢵⠃⠀⠀⠀⠀⠀⢀⠀⠀⠀⢀⠀⠀
        # ⠀⠀⠀⠀⠀⠄⠀⠂⠀⠀⠀⠀⡀⢈⢮⡂⠱⡱⠥⣝⢵⢫⢞⢮⣗⢽⡪⡪⢦⣕⢝⡵⣑⢮⣳⢯⠃⠀⠀⠀⠀⠀⠁⠀⠀⠀⠁⠀⠀⠀
        # ⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⢠⢣⡻⡰⡑⢕⢎⡳⣹⢓⢧⡫⣮⣫⣝⢷⣪⣻⣪⢗⡷⣝⠂⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠠
        # ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢔⢇⡟⣼⢱⢌⠪⠸⡕⣝⢪⢎⢶⢕⣯⣫⢷⡽⣮⣟⡽⡂⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠁⠀⠐⠀⠀
        # ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⢀⠎⡐⣕⢽⡸⣣⢗⢵⡙⡦⡱⡘⢆⢳⡱⢳⢜⢷⣫⢿⢾⢮⠯⠀⡀⠂⠄⠠⠀⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀
        # ⠀⠀⠀⠀⠀⠂⠈⠀⠂⡔⠡⢢⢜⡼⣱⡫⣞⢕⢗⢼⡪⣚⢝⢮⣢⢕⡱⡙⢮⠳⡫⠳⠋⠁⠂⠠⠂⡐⢀⠡⢈⠀⡁⠄⠠⠀⠂⠀⠠⠀
        # ⠀⠐⠀⠁⠀⠁⠀⠀⢑⢜⢕⡕⣕⢷⡱⣝⢮⣹⢣⢗⡝⣮⡫⣞⢼⢵⣝⢿⡫⠁⠠⠀⠌⢀⠁⡐⠀⠠⢀⠀⠂⠐⠀⠂⠐⡈⠠⠁⠄⠠
        # ⠀⠠⠀⠐⠀⠀⠁⢀⠀⠱⡫⢮⡪⡳⣝⢞⣧⢫⣗⢯⡺⣮⢳⣝⢷⣳⡟⢁⠀⠂⠄⠨⠀⠠⠀⠄⠂⠐⡀⠈⠄⢁⠈⡀⢁⠀⠐⠀⠌⠐
                
        # Let's scare him away with a job application!
        
        #  ___________
        # | MCDONALDS |
        # | - $12/hr  |
        # | ~~~~ ~~ ~ |
        # | ~ ~~~ ~~  |
        # | ~~ ~~~~   |
        # | ~~~ ~ ~~~ |
        # '-----------'
        
        # Okay good he's gone.
        
        # Anyway, now we're onto Step 3: finding the cofactors.
        
        workingContents[0][1] = 0 - workingContents[0][1]
        workingContents[1][0] = 0 - workingContents[1][0]
        workingContents[1][2] = 0 - workingContents[1][2]
        workingContents[2][1] = 0 - workingContents[2][1]
        
        # Luckily, this step isn't as carcinogenic to program as the last step.
        # We're just flipping the signs of some of the elements in a checkerboard pattern.
        
        # Like this:
        
        # [ [ 1, 1, 1 ],       We're gonna overlay this, and flip each element which lines up with a minus sign. (-)
        #   [ 1, 1, 1 ], 
        #   [ 1, 1, 1 ] ]      [ [ +, -, + ],
        #                        [ -, +, - ],
        #                        [ +, -, + ] ].
        
        #                      This gives us [ [ 1, -1, 1 ], 
        #                                      [ -1, 1, -1 ], 
        #                                      [ 1, -1, 1 ] ]
        
        #                      These are called our cofactors!
        
        # Thankfully, we only actualy change four of the elements, so we can just flip those and leave the rest.
        
        # Step 4: Transpose our cofactors, and divide them by our determinant from step 1.
        # This one's fairly easy.
        
        transposedCofactors = [] # Yes, this is copied from get_transpose(). 
                                 # I just didn't want to instantiate a whole new matrix object only to run get_contents() on it. 
        
        for i in range(3):
            row = []
            
            for j in range(3):
                row.append(workingContents[j][i])
            transposedCofactors.append(row)
        
        try:
            return Matrix(transposedCofactors).multiply_contents(1 / det)
        except:
            print("This matrix is probably singular, so an inverse couldn't be found.")
            
        # Thank god it's over! I hope your enjoyed our munity through 3x3 matrix inversion.
        # I'm probably not going to mansplain as much in the rest of my code but for other complex
        # functions I'll get my dreaded comments out again.
        
    def add(self, matrixToAddIdk):
        if self.order != matrixToAddIdk.get_order():
            print("These have different orders dumbass you can't add them")
            return None
        
        contentsToAdd = matrixToAddIdk.get_contents()
        
        result = []
        
        for row in range(self.order[0]):
            result.append([])
            
            for collumb in range(self.order[1]):
                result[row].append(self.contents[row][collumb] + contentsToAdd[row][collumb])
        
        return Matrix(result)
    
    def subtract(self, matrixToSubtractIdk): # This looks completely useless and honestly I thought the same,
                                             # but it's cumbersome manually negating a matrix every time you
                                             # want to subtract it, so this should be a little bit faster
        if self.order != matrixToSubtractIdk.get_order():
            print("These have different orders dumbass you can't subtract them")
            return None
        
        contentsToSubtract = matrixToSubtractIdk.get_contents()
        
        result = []
        
        for row in range(self.order[0]):
            result.append([])
            
            for collumb in range(self.order[1]):
                result[row].append(self.contents[row][collumb] - contentsToSubtract[row][collumb])
        
        return Matrix(result)

    def apply(self, right): # Matrix multiplication isn't commutative, so we have one
                            # on the left, and one on the right.
                
                            # "self" is on the left. Can you guess where "right" is?

                            # A: Also on the left
                            # B: Idk
                            # C: Please stop leaving these comments
                            # D: On the right

                            # If you picked D, that's correct well done!!! If you picked
                            # A or B then here's your participation award: 

                            #   _______
                            #  |       |
                            # (|  NOT  |)
                            #  | QUITE!|
                            #   \     /
                            #    `---'
                            #    _|_|_

                                             # I'm not fucking getting the contents from
        rightContents = right.get_contents() # each object every single time idc about 
                                             # memory efficiency

        if self.get_order()[1] != right.get_order()[0]:
            print(f"The matrices {self} and {right} can't be applied!")
            return None # SEe? I can do input validation!!!

        productOrder = (self.get_order()[0], right.get_order()[1])
        collumbLength = self.get_order()[1]
        workingContents = []
                    
        for row in range(productOrder[0]):
            workingContents.append([])

            for collumb in range(productOrder[1]):
                scalarProduct = 0
                for i in range(collumbLength):                
                    scalarProduct += self.contents[row][i] * rightContents[i][collumb]

                workingContents[row].append(scalarProduct)

        return Matrix(workingContents)


# Some usefull constants before we move on

# Identity matrices
I2 = Matrix([[1, 0], 
             [0, 1]])

I3 = Matrix([[1, 0, 0], 
             [0, 1, 0], 
             [0, 0, 1]])

# Origin vector
ORIGIN = Matrix([[0], 
                 [0], 
                 [0]])



# ---------------- ABSTRACTS ----------------

class Abstract:
    def __init__(self, 
                 
                 name:str=None,
                 
                 location:Matrix=None, 
                 
                 distortion:Matrix=None, 
                 
                 tags:list[str]=None,
                 
                 parent=None, 
                 
                 children=None, 
                 
                 script=None): # I'm well aware this is clapped. 
        
                             # Unfortunately for people unlucky enough to see this, default values in Python
                             # are created at the definition of the function, instead of when it's called. 
                
                             # This means if I assign default values in the parameter list, EVERY abstract 
                             # that uses those default values will then share those parameters, even when I 
                             # change them.
                             
                             # Guess how long it took to find that out while debugging.
        
        self.name = "Abstract" if not name else name # I hate If Expressions too if that's any consolation
        
                                                     # Sorry, I mean
                                                     
                                                     # if that's any consolation:
                                                     #     I hate If Expressions too
        
        self.parent = parent if parent else None
        self.children = children if children else []
        
        if parent:
            self.objectiveLocation = self.parent.objectiveLocation.add(self.parent.objectiveDistortion.apply(location if location else ORIGIN))
            self.objectiveDistortion = self.parent.objectiveDistortion.apply(distortion if distortion else I3) 
            
            # That looks confusing but it just generates the appropriate objective
            # location such that it's at the position you entered relative to its
            # superstract.
            
            # If you're wondering why I don't just store the relative locations, it's
            # becasue I tried it and it was slow.
                
            # In every raster cycle, you need to find the positions of every vertex
            # relative to the camera. With objective coordinates being stored, you
            # just have to read those from memory and compare them. However, with
            # relative coordinates I had to make a recursive function which
            # would spend four fucking years every frame traversing all the way up
            # the scene tree to the objective origin doing matrix applications for
            # each link.
            
            # While storing it like this makes it harder to find local coordinates,
            # you only need to compare the current abstract with its superstract
            # to find them, whereas finding objective coordinates with stored 
            # coordinates in local space requires analysing the entire scene tree.
            
            
        else:
            self.objectiveLocation =  location if location else ORIGIN
            self.objectiveDistortion = distortion if distortion else I3

        self.script = None # Implement this later
        
        self.tags = tags if tags else []
        
        
        
    def get_name(self):
        return self.name
    
    def set_name(self, name: str):
        self.name = name
        
        
        
    def get_tags(self):
        return self.tags
    
    def add_tag(self, tag:str):
        self.tags.append(tag)
    
    def remove_tag(self, tag:str):
        self.tags.remove(tag)
        
    def check_for_tag(self, tag:str):
        return tag in self.tags
    
    def get_substracts_with_tag(self, tag:str):
        found = []
        for child in self.children:
            if child.check_for_tag(tag):
                found.append(child)
                
            found += child.get_substracts_with_tag(tag)
            
        return found
        
    
    
    def get_type(self):
        return self.__class__
    
    def get_substracts_of_type(self, type):
        found = []
        for child in self.children:
            if child.__class__ == type:
                found.append(child)
                
            found += child.get_substracts_of_type(type)
            
        return found
        
        
    # Heirachy functions
        
    def get_parent(self):
        return self.parent
    
    def set_parent(self, newParent):
        if self.parent:
            self.parent.children.remove(self)
        self.parent = newParent
            
        if not self in newParent.children:
            newParent.children.append(self)
        
        
        
    def get_children(self):
        return self.children
    
    def add_child(self, newChild):
        if newChild.parent:
            newChild.parent.children.remove(newChild)
        newChild.parent = self
        
        if not newChild in self.children:
            self.children.append(newChild)
        
    def remove_child(self, child):
        if self.parent:
            child.parent = self.parent
        else:
            return
            
        self.children.remove(child)

        self.parent.children.append(child)
        
        

    def kill_self(self): # This is figurative and does not need to be shown to Pastoral
        if self.parent:
            for child in self.children:
                child.parent = self.parent

            self.parent.remove_child(self)  
            
            del self
        else:
            print("Why tf are you trying to delete the origin? Not cool man")

    def kill_self_and_children(self): # Neither does this
        if self.children:
            for child in self.children:
                child.delete_self_and_children()
        
        if self.parent:
            self.parent.children.remove(self)
        
        del self


    # Transform functions
        
    def get_objective_location(self):
        return self.objectiveLocation
    
    def set_objective_location(self, location):
        self.objectiveLocation = location
        
        
        
    def get_objective_distortion(self):
        return self.objectiveDistortion
    
    def set_objective_distortion(self, distortion):
        self.objectiveDistortion = distortion
        
    
    
    def get_relative_location(self):
        if self.parent:
            return self.parent.objectiveDistortion.get_3x3_inverse().apply(self.objectiveLocation.subtract(self.parent.objectiveLocation))
        else:
            return self.objectiveLocation
        
    def set_relative_location(self, location):
        if self.parent:
            self.objectiveLocation = self.parent.objectiveLocation.add(self.parent.objectiveDistortion.apply(location))
        else:
            self.objectiveLocation = location
            
    def get_relative_distortion(self):
        if self.parent:
            return self.parent.objectiveDistortion.get_3x3_inverse().apply(self.objectiveDistortion)
    
    def set_relative_distortion(self, distortion):
        if self.parent:
            self.objectiveDistortion = self.parent.objectiveDistortion.apply(distortion)
        else:
            self.objectiveDistortion = distortion
        
        

    def translate_objective(self, vector):
        self.objectiveLocation = self.objectiveLocation.add(vector)

    def rotate_euler_radians(self, x, y, z): # This follows the order yxz
        sinx = math.sin(x)
        cosx = math.cos(x)
        siny = math.sin(y)
        cosy = math.cos(y)
        sinz = math.sin(z)
        cosz = math.cos(z)

        print(sinx, cosx, siny, cosy, sinz, cosz)
        
        self.set_relative_distortion(Matrix([[cosz, -sinz, 0], # This is wrong, fix later
                                             [sinz, cosz, 0],
                                             [0, 0, 1]]).apply(
                                      
                                     Matrix([[1, 0, 0],
                                             [0, cosx, -sinx],
                                             [0, sinx, cosx]])).apply(
                                     Matrix([[cosy, 0, siny],
                                             [0, 1, 0],
                                             [-siny, 0, cosy]])).apply(self.get_relative_distortion()))
                            
# Important default abstracts:

ROOT = Abstract("Root")

    

# ---------------- GRAPHICS OBJECTS ----------------

# Pygame Setup - initialises the window, 
pygame.init()
window = pygame.display.set_mode((320, 240))
clock = pygame.time.Clock()
running = True

class Tri(Abstract): # This should be a child to an abstract which will serve as a wrapper for a group of polys.
    def __init__(self, vertices, albedo, lit: bool):   
        super().__init__("Tri", ORIGIN, I3, ["Tri"])
        
        # Vertices should be an array of 3 arrays.
                                            # Each array is a coordinate, done in clockwise 
                                            # order if you're looking at the opaque side.

                                            # This gets converted to a 3x3 matrix with each
                                            # collumb being a coordinate.

                                            # Is this really annoying? Yes!
                                            # But it makes it easier to apply transformation 
                                            # matrices to polygons so I'll just hate myself later 

        self.vertices = Matrix(vertices).get_transpose()
        self.albedo = albedo
        self.lit = lit
        
    def get_vertices(self):
        return self.vertices
    
    def set_vertices(self, vertices):
        self.vertices = vertices
        
class Camera(Abstract):
    def __init__(self, name, location, distortion, perspectiveConstant):
        super().__init__(name, location, distortion, ["Camera"])
        self.perspectiveConstant = perspectiveConstant
        
    def project_tri(self, cameraLocationMatrix, inversion, tri):
        triLocation = tri.get_objective_location().get_contents()
        triLocationMatrix = Matrix([[triLocation[0][0], triLocation[0][0], triLocation[0][0]],
                                 [triLocation[1][0], triLocation[1][0], triLocation[1][0]],
                                 [triLocation[2][0], triLocation[2][0], triLocation[2][0]]])

        triObjectiveVertices = tri.get_objective_distortion().apply(tri.get_vertices()).add(triLocationMatrix)
        
        triCameraVertices = inversion.apply(triObjectiveVertices.subtract(cameraLocationMatrix)).get_contents()
        
        if triCameraVertices[2][0] > 0 and triCameraVertices[2][1] > 0 and triCameraVertices[2][2] > 0:
            screenSpaceCoordinates = (
                (triCameraVertices[0][0] / (triCameraVertices[2][0] * self.perspectiveConstant) + 160, 
                triCameraVertices[1][0] / (triCameraVertices[2][0] * self.perspectiveConstant) + 120),
                
                (triCameraVertices[0][1] / (triCameraVertices[2][1] * self.perspectiveConstant) + 160, 
                triCameraVertices[1][1] / (triCameraVertices[2][1] * self.perspectiveConstant) + 120),
                
                (triCameraVertices[0][2] / (triCameraVertices[2][2] * self.perspectiveConstant) + 160, 
                triCameraVertices[1][2] / (triCameraVertices[2][2] * self.perspectiveConstant) + 120)
            )
            
            pygame.draw.polygon(window, tri.albedo, screenSpaceCoordinates)
        
        
        
    def rasterize(self):
        tris = ROOT.get_substracts_of_type(Tri)
        
        inversion = self.objectiveDistortion.get_3x3_inverse()
        location = self.objectiveLocation.get_contents()
        locationMatrix = Matrix([[location[0][0], location[0][0], location[0][0]],
                                 [location[1][0], location[1][0], location[1][0]],
                                 [location[2][0], location[2][0], location[2][0]]])
        
        for tri in tris:
            self.project_tri(locationMatrix, inversion, tri)
        
    

  
'''          
testMatrix = Matrix([[3, -1, 3.4],
                     [0, -4.5, 1],
                     [7, 3, 2]])

testVector = Matrix([[1],
                     [-25],
                     [0.5]])


origin = Abstract("origin", Matrix([[1], # Abstract 1
                          [1],
                          [1]]), Matrix([[0, 0, 1],
                                         [0, 1, 0],
                                         [-1, 0, 0]]))

childAbstract = Abstract(None, None, None, ["Rose toy"])

childChildAbstract = Abstract("childChild", Matrix([[1], # Abstract 2
                                                    [1],
                                                    [1]]), Matrix([[1, 0, 0],
                                                                   [0, 2, 0],
                                                                   [0, 0, 1]]), ["Rose toy"])

origin.add_child(childAbstract)
childAbstract.add_child(childChildAbstract)

print(origin.get_substracts_with_tag("Rose toy"))'''

origin = Abstract("Origin")

ROOT.add_child(origin)

camera = Camera("Main camera", Matrix([[0],
                                       [0],
                                       [-4]]), I3, 0.005)
origin.add_child(camera)

movementSpeed = 1.5

mesh = Abstract("Mesh", ORIGIN, Matrix([[2, 0, 0],
                                        [0, 1, 0],
                                        [0, 0, 1]]))
origin.add_child(mesh)

for i in range(50):
    n = Tri([[random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)],
             [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)],
             [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)]],
                        
            (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
            
            True)
    mesh.add_child(n)
    
frameDelta = 0

while running:
    startTime = time.time()
    
    events = pygame.event.get()
    
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        camera.translate_objective(Matrix([[0],
                                    [0],
                                    [movementSpeed * frameDelta]]))
    elif keys[pygame.K_s]:
        camera.translate_objective(Matrix([[0],
                                    [0],
                                    [-movementSpeed * frameDelta]]))
        
    if keys[pygame.K_a]:
        camera.translate_objective(Matrix([[-movementSpeed * frameDelta],
                                    [0],
                                    [0]]))
    elif keys[pygame.K_d]:
        camera.translate_objective(Matrix([[movementSpeed * frameDelta],
                                    [0],
                                    [0]]))
    
    if keys[pygame.K_RIGHT]:
        camera.rotate_euler_radians(0, 1 * frameDelta, 0)
    elif keys[pygame.K_LEFT]:
        camera.rotate_euler_radians(0, -1 * frameDelta, 0)

    
    mesh.rotate_euler_radians(1 * frameDelta, 1 * frameDelta, 0)

    window.fill((255, 255, 255))

    camera.rasterize()
        
    frameDelta = time.time() - startTime

    try:
        print(f"Finished frame calculation test in {frameDelta} seconds. \nEquivalent to {1 / (frameDelta)} Hz")
    except:
        print("Very fast")
        
    pygame.display.flip()