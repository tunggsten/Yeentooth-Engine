import pygame

import math
import random
import time



# ---------------- MATHEMATICAL CONSTRUCTS ----------------

def clamp(val:float, min:float, max:float): # the math library didn't have a function to do this so 
    if val > max:                           # I have to pick up their slack
        return max
    elif val < min:
        return min
    else:
        return val



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
    
    def get_magnitude(self): # This only works on collumb vectors
        numberOfCollumbs = len(self.contents)
        workingMagnitude = 0

        for i in range(numberOfCollumbs):
            workingMagnitude += self.contents[i][0] ** 2
        
        workingMagnitude = math.sqrt(workingMagnitude)

        return workingMagnitude
    
    def set_magnitude(self, newMagnitude:float=1): # This makes the magnitude of a collumb vector 1 by default, or a different value if specified
        currentMagnitude = self.get_magnitude()

        newContents = []

        if currentMagnitude != 0:
            ratio = newMagnitude / currentMagnitude

            for content in self.contents:
                newContents.append([content[0] * ratio])

        else:
            for content in self.contents:
                newContents.append([0])
        
        return Matrix(newContents)
         
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

        if det == 0:
            return Matrix([[1, 0, 0],
                           [0, 1, 0],
                           [0, 0, 1]])
        
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
        
        return Matrix(transposedCofactors).multiply_contents(1 / det)
            
        # Thank god it's over! I hope your enjoyed our munity through 3x3 matrix inversion.
        # I'm probably not going to mansplain as much in the rest of my code but for other complex
        # functions I'll get my dreaded comments out again.
        
    def add(self, matrixToAddIdk):
        if self.order != matrixToAddIdk.get_order():
            print(f"{self.get_contents()} and {matrixToAddIdk.get_contents()} have different orders dumbass you can't add them")
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
            print(f"The matrices {self.get_contents()} and {right.get_contents()} can't be applied!")
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
                 script=None,
                 parent=None, 
                 children=None): # I'm well aware this is clapped. 
        
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

        self.script = script if script else None # Implement this later
        
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
    
    def get_children_with_tag(self, tag:str):
        found = []
        for child in self.children:
            if child.check_for_tag(tag):
                found.append(child)
        
        return found
    
    def get_substracts_with_tag(self, tag:str):
        found = []
        for child in self.children:
            if child.check_for_tag(tag):
                found.append(child)
                
            found += child.get_substracts_with_tag(tag)
            
        return found
        
    
    
    def get_type(self):
        return self.__class__
    
    def get_children_of_type(self, type): # Children are the abstracts directly underneath an abstract
        found = []
        for child in self.children:
            if child.__class__ == type:
                found.append(child)

        return found
    
    def get_substracts_of_type(self, type): # Substracts are all abstracts underneath an abstract,
        found = []                          # meaning its children, its children's children, etc.
        for child in self.children:
            if child.__class__ == type:     # The same applies to parents and superstracts;
                found.append(child)         # parents are directly above, superstracts are everything
                                            # above
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
    
    def get_substracts(self):
        substracts = self.get_children()
        for child in self.children:
            substracts += child.get_substracts()

        return substracts
    
    def add_child_relative(self, newChild):
        print(f"Adding child: {newChild.get_name()} at {newChild.objectiveLocation}")
        if newChild.parent:
            newChild.parent.children.remove(newChild)
        newChild.parent = self

        newChild.set_location_relative(newChild.objectiveLocation)
        newChild.set_distortion_relative(newChild.objectiveDistortion)
        
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

    def kill_self_and_substracts(self): # Neither does this
        if self.children:
            for child in self.children:
                child.delete_self_and_substracts()
        
        if self.parent:
            self.parent.children.remove(self)
            del self

    

    # Transform functionsDO NOT TOUCH EVER!!!!!!!!!!!11🚫🚫🚫🚫🚫🚫🚫🚫
    # ⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔☣️☣️☣️☣️☣️☣️☣️☣️☣️☣️☣️
    # ☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️
    # THIS TOOK FOUR FUCKING DAYS TO DEBUG THE LAST TIME IT BROKE

    # Location functions 

    # Objective

    def get_location_objective(self):
        return self.objectiveLocation

    def set_location_objective(self, location:Matrix):
        vector = location.subtract(self.objectiveLocation)

        self.objectiveLocation = location

        for child in self.get_children():
            child.translate_objective(vector)
    
    def translate_objective(self, vector:Matrix):
        self.objectiveLocation = self.objectiveLocation.add(vector)

        for child in self.get_children():
            child.translate_objective(vector)

    # Relative

    def get_location_relative(self):
        if self.parent:
            return self.parent.objectiveDistortion.get_3x3_inverse().apply(self.objectiveLocation.subtract(self.parent.objectiveLocation))
            # This subtracts the parent's location to move the origin to the parent, and then reverses the
            # parent's distortion to get the relative coordinate
        else:
            return self.objectiveLocation
            # If it has no parent, it must be the root, so we just have to find it's objective location

    def set_location_relative(self, location:Matrix):
        if self.parent:
            self.set_location_objective(self.parent.objectiveDistortion.apply(location).add(self.parent.objectiveLocation))
            # This starts by distorting the location to make it relative to the parent's axes, and then
            # moves it from the objective origin to the parent
        else:
            self.set_location_objective(location)

    def translate_relative(self, vector:Matrix):
        if self.parent:
            self.translate_objective(self.objectiveDistortion.apply(vector))
            # We only need to apply the distortion here, because vector is just a 
            # direction and a magnitude instead of being a point in space
        else:
            self.translate_objective(vector)



    # Distortion functions (I've spent four days and counting debugging these)

    # Objective

    def get_distoriton_objective(self):
        return self.objectiveDistortion
        
    def set_distortion_objective(self, distortion:Matrix, pivot:Matrix=None):
        distortionPivot = pivot if pivot else self.objectiveLocation

        transformation = distortion.apply(self.objectiveDistortion.get_3x3_inverse())

        # That's the distortion matrix you have to apply to skew the current distortion
        # to the target one. This works because:

        # [transformation][currentDistortion] has to equal [targetDistortion]    <--------------------------------
        #                                                                                                        |
        # We can apply the inverse of the current distortion on the right                                        |
        # of both sides of the equation without making it invalid                                                |          This stupid fucking arrow
        #                                                                                                        |          took longer to make than
        # [transformation][currentDistortion][currentDistortion]^-1 = [targetDistortion][currentDistortion]^-1   |          everything else in this 
        #                                                                                                        |          explanation
        # Then [currentDistortion][currentDistortion]^-1 cancel out to make I3, which doesn't change             |          
        # matrices when it's applied to them.                                                                    |
        #                                                                                                        |
        # Therefore ----------------------------------------------------------------------------------------------

        self.objectiveDistortion = distortion
        self.objectiveLocation = transformation.apply(self.objectiveLocation.subtract(distortionPivot)).add(distortionPivot)

        # That last line changed the abstract's location to move it round the pivot point.
        # Most of the time you won't need a pivot, but it's used when this recurrs over
        # an abstract's substracts.

        # That worked because:

        # Applying a transformation matrix to a point transforms it relative to the origin.

        # |                   /
        # |    x      --->   /    x
        # |                 /
        # +--------        /-------- 

        # Therefore, if we want to transform around a pivot thats' not the origin,
        # we can subtract the location of a pivot from the point's location
        # so the new location of the point is what it's location relative to the 
        # pivot was.

        # |     x                                           |          
        # |          subtract location of p from everything | x        Now p is
        # |   p                        --->                 |          the origin.
        # +--------                                         p--------

        # *Now* we can apply our transformation, because we've effectively mored the
        # origin to the pivot. Then, we just move the origin back by adding the
        # pivot's location back to everything.

        for child in self.children:
            child.distort_objective(transformation, distortionPivot) # This makes all the substracts
                                                           # move to keep their relative
                                                           # transforms

    def distort_objective(self, transformation:Matrix, pivot:Matrix=None):
        distortionPivot = pivot if pivot else self.objectiveLocation

        self.objectiveDistortion = transformation.apply(self.objectiveDistortion)
        self.objectiveLocation = transformation.apply(self.objectiveLocation.subtract(distortionPivot)).add(distortionPivot)

        for child in self.children:
            child.distort_objective(transformation, distortionPivot)

    # Relative

    def get_distortion_relative(self):
        if self.parent:
            return self.parent.objectiveDistortion.get_3x3_inverse().apply(self.objectiveDistortion)
            # Here we just undo the parent's distortion
        else:
            return self.objectiveDistortion
        
    def set_distortion_relative(self, distortion):
        if self.parent:
            self.set_distortion_objective(self.parent.objectiveDistortion.apply(distortion))
        else:
            self.set_distortion_objective(distortion)

    def distort_relative(self, transformation):
        if self.parent:
            self.distort_objective(self.parent.objectiveDistortion.apply(transformation).apply(self.parent.objectiveDistortion.get_3x3_inverse()))
            # We need to appply the inverse at the end of this function but *not* set_distortion_relative
            # becasue reasons. I'll be entirely honest idfk why I just applied the inverse on a whim while
            # bug fixing and it worked but it fucked up set_distortion_relative when I put it on there

            # I think it's something do with how transformation is a difference and it isn't relative to 
            # actual points?
        else:
            self.distort_objective(transformation)
    


    # Rotation functions
        
    def rotate_euler_radians(self, x:float, y:float, z:float): # This follows the order yxz
        sinx = math.sin(x)
        cosx = math.cos(x)
        siny = math.sin(y)
        cosy = math.cos(y)
        sinz = math.sin(z)
        cosz = math.cos(z)
        
        rotationMatrix = Matrix([[cosz, -sinz, 0], # This is wrong, fix later
                                 [sinz, cosz, 0],
                                 [0, 0, 1]]).apply(
                         
                         Matrix([[1, 0, 0],
                                 [0, cosx, -sinx],
                                 [0, sinx, cosx]])).apply(
                                     
                         Matrix([[cosy, 0, siny],
                                 [0, 1, 0],
                                 [-siny, 0, cosy]]))
        
        self.distort_relative(rotationMatrix) # Change back to relative when it's fixed

    

    # Scripting functions

    def run_script(self):
        if self.script:
            exec(open(self.script, "r"))

    def attach_script(self, script):
        self.script = script

    def get_script_path(self):
        return self.script
    
    def initialise_script(self):
        pass

    def initialise_process(self):
        self.initialise_script()

        for child in self.children:
            child.initialise_process()
    
    def process(self):
        self.run_script()

        for child in self.children:
            child.process()
        

                            
# Important default abstracts:

ROOT = Abstract("Root")

    

# ---------------- GRAPHICS OBJECTS ----------------

# Pygame Setup - initialises the window

# I'm doing this here because some of the graphics abstracts
# have to reference these

pygame.init()
SCREENSIZE = (640, 510)
SCREENSIZEFROMCENTER = (SCREENSIZE[0] / 2, SCREENSIZE[1] / 2)
window = pygame.display.set_mode(SCREENSIZE)
pygame.display.set_caption("yeentooth")
clock = pygame.time.Clock()
engineRunning = True

class Image(): # This is like a shitty fake version of pygame.Surface
    def __init__(self, position:tuple, resolution:tuple, pixelSize:tuple, colorspace:bool):
        self.position = position
        self.resolution = resolution
        self.pixelSize = pixelSize
        self.colorspace = colorspace
        
        if colorspace:
            pixel = (0, 0, 0)
        else:
            pixel = 0.0

        self.contents = []
        for row in range(resolution[1]):
            self.contents.append([])
            for pixel in range(resolution[0]):
                self.contents[row].append((0, 0, 0) if colorspace else 0.0)

    def set_position(self, position:tuple):
        self.position = position

    def get_position(self):
        return self.position

    def set_resolution(self, resolution:tuple):
        self.resolution = resolution

        self.contents = [[self.colorspace] * self.resolution[0]] * self.resolution[1]
    
    def get_resolution(self):
        return self.resolution
    
    def set_pixel_size(self, pixelSize:tuple):
        self.pixelSize = pixelSize

    def fill(self, value):
        for i in range(self.resolution[1]):
            for j in range(self.resolution[0]):
                self.contents[i][j] = value

    def interpolate_colour(self, colour1:tuple, colour2:tuple, t:float):
        return (math.floor(colour1[0] + (colour2[0] - colour1[0]) * abs(t)),
                math.floor(colour1[1] + (colour2[1] - colour1[1]) * abs(t)),
                math.floor(colour1[2] + (colour2[2] - colour1[2]) * abs(t)))
    
    def interpolate_value(self, float1:float, float2:float, t:float):
        return float1 + (float2 - float1) * abs(t)
    
    

    def draw_horizontal_coloured_line(self, 
                                      x1:int, 
                                      x2:int, 
                                      y:int,
                                      depthBuffer, 
                                      depth1:float,
                                      depth2:float, 
                                      colour1:tuple, 
                                      colour2:tuple=None):
        if 0 <= y < self.resolution[1]:
            for i in range(x1, x2, 1 if x1 < x2 else -1):
                if 0 <= i < self.resolution[0]:
                    interpolationAmount = (i - x1) / abs(x2 - x1)
                    depth = self.interpolate_value(depth1, depth2, interpolationAmount)
                    
                    if depth < depthBuffer.contents[y][i]:
                        if colour2:
                            pixelColour = self.interpolate_colour(colour1, colour2, interpolationAmount)
                            self.contents[y][i] = pixelColour
                            depthBuffer.contents[y][i] = depth
                        else:
                            self.contents[y][i] = colour1
                            depthBuffer.contents[y][i] = depth
                            
                            

    def draw_flat_based_coloured_triangle(self, 
                                          bottomLeft:tuple, 
                                          bottomRight:tuple, 
                                          point:tuple, 
                                          depthBuffer,
                                          depth1:float,
                                          depth2:float,
                                          depth3:float,
                                          colour1:tuple, 
                                          colour2:tuple=None, 
                                          colour3:tuple=None):
        height = point[1] - bottomLeft[1]
        leftToPoint = bottomLeft[0] - point[0]
        rightToPoint = bottomRight[0] - point[0]
         
        for y in range(bottomLeft[1], point[1], 1 if height > 0 else -1):
            amountDone = abs((y - bottomLeft[1]) / height)

            left = math.floor(bottomLeft[0] - (leftToPoint * amountDone))
            right = math.floor(bottomRight[0] - (rightToPoint * amountDone))
            
            leftDepth = self.interpolate_value(depth1, depth3, amountDone)
            rightDepth = self.interpolate_value(depth2, depth3, amountDone)

            if colour2:
                self.draw_horizontal_coloured_line(left, right, y, depthBuffer, leftDepth, rightDepth, 
                                        self.interpolate_colour(colour1, colour3, amountDone), 
                                        self.interpolate_colour(colour2, colour3, amountDone))
            else:
                self.draw_horizontal_coloured_line(left, right, y, depthBuffer, leftDepth, rightDepth, colour1)
                
                

    def draw_coloured_triangle(self, 
                               vertex1:tuple,
                               vertex2:tuple,
                               vertex3:tuple,
                               depthBuffer,
                               depth1:float,
                               depth2:float,
                               depth3:float,
                               colour1:tuple,
                               colour2:tuple=None,
                               colour3:tuple=None):
        
        # Find the middle vertex
        heights = [vertex1[1], vertex2[1], vertex3[1]]
        
        if colour2:
            if heights[0] > heights[1]:
                if heights[0] > heights[2]:
                    if heights[1] > heights[2]:
                        vertices = [vertex1, vertex2, vertex3]
                        colours = [colour1, colour2, colour3]
                        depths = [depth1, depth2, depth3]
                    else:
                        vertices = [vertex1, vertex3, vertex2]
                        colours = [colour1, colour3, colour2]
                        depths = [depth1, depth3, depth2]
                else:
                    vertices = [vertex3, vertex1, vertex2]
                    colours = [colour3, colour1, colour2]
                    depths = [depth3, depth1, depth2]
            else:
                if heights[0] < heights[2]:
                    if heights[1] < heights[2]:
                        vertices = [vertex3, vertex2, vertex1]
                        colours = [colour3, colour2, colour1]
                        depths = [depth3, depth2, depth1]
                    else:
                        vertices = [vertex2, vertex3, vertex1]
                        colours = [colour2, colour3, colour1]
                        depths = [depth2, depth3, depth2]
                else:
                    vertices = [vertex2, vertex1, vertex3]
                    colours = [colour2, colour1, colour3]
                    depths = [depth2, depth1, depth3]
        else:
            if heights[0] > heights[1]:
                if heights[0] > heights[2]:
                    if heights[1] > heights[2]:
                        vertices = [vertex1, vertex2, vertex3]
                        depths = [depth1, depth2, depth3]
                    else:
                        vertices = [vertex1, vertex3, vertex2]
                        depths = [depth1, depth3, depth2]
                else:
                    vertices = [vertex3, vertex1, vertex2]
                    depths = [depth3, depth1, depth2]
            else:
                if heights[0] < heights[2]:
                    if heights[1] < heights[2]:
                        vertices = [vertex3, vertex2, vertex1]
                        depths = [depth3, depth2, depth1]
                    else:
                        vertices = [vertex2, vertex3, vertex1]
                        depths = [depth2, depth3, depth2]
                else:
                    vertices = [vertex2, vertex1, vertex3]
                    depths = [depth2, depth1, depth3]
            
        # Don't ask

        triangleHeight = vertices[0][1] - vertices[2][1]
        topToBottomHorizontal = vertices[0][0] - vertices[2][0]

        if triangleHeight > 0:
            sliceAmount = (vertices[1][1] - vertices[2][1]) / triangleHeight
        else:
            sliceAmount = 0
        
        sliceCoordinate = (math.floor(vertices[2][0] + (topToBottomHorizontal * (sliceAmount))), vertices[1][1])
        sliceDepth = self.interpolate_value(depths[0], depths[2], 1 - sliceAmount)
        
        if colour2:
            sliceColour = self.interpolate_colour(colours[0], colours[2], 1 - sliceAmount)

            self.draw_flat_based_coloured_triangle(vertices[1], sliceCoordinate, vertices[2], 
                                                   depthBuffer, depths[1], sliceDepth, depths[2],
                                                   colours[1], sliceColour, colours[2])
            self.draw_flat_based_coloured_triangle(vertices[1], sliceCoordinate, vertices[0], 
                                                   depthBuffer, depths[1], sliceDepth, depths[0],
                                                   colours[1], sliceColour, colours[0])
        else:
            self.draw_flat_based_coloured_triangle(vertices[1], sliceCoordinate, vertices[2], 
                                                   depthBuffer, depths[1], sliceDepth, depths[2],
                                                   colour1)
            self.draw_flat_based_coloured_triangle(vertices[1], sliceCoordinate, vertices[0],
                                                   depthBuffer, depths[1], sliceDepth, depths[0],
                                                   colour1)
        
                

    def render_image(self, target:pygame.Surface):
        for row in range(self.resolution[1]):
            for pixel in range(self.resolution[0]):
                pygame.draw.rect(target, 
                                 self.contents[row][pixel], 
                                 pygame.Rect((pixel * self.pixelSize[0] + self.position[0], row * self.pixelSize[1] + self.position[1]), self.pixelSize))

    def render_depthbuffer(self, target, position):
        for row in range(self.resolution[1]):
            for pixel in range(self.resolution[0]):
                pygame.draw.rect(target, 
                                 (clamp(self.contents[row][pixel] * 25, 0, 255), 
                                  clamp(self.contents[row][pixel] * 25, 0, 255),
                                  clamp(self.contents[row][pixel] * 25, 0, 255)),
                                 pygame.Rect((pixel * self.pixelSize[0] + self.position[0], row * self.pixelSize[1] + self.position[1]), self.pixelSize))



# This will be the colour display triangles get rendered to

DISPLAY = Image((0, 30), (128, 96), (5, 5), True)
DEPTHBUFFER = Image((0, 0), (128, 96), (5, 5), False)



class Tri(Abstract): # This should be a child to an abstract which will serve as a wrapper for a group of polys.
    def __init__(self, 
                 vertices:list[list[float]], 
                 albedo:tuple, lit:bool, tags:list[str]=None):   
        super().__init__("Tri", ORIGIN, I3, ["Tri"] + tags if tags else [])
        
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

    def get_albedo(self):
        return self.albedo
    
    def set_albedo(self, albedo:tuple):
        self.albedo = albedo
        


class GradientTri(Tri): # This is just a tri with coloured vertices instead of a flat colour
    def __init__(self,
                 vertices:list[list[float]], 
                 albedo1:tuple,
                 albedo2:tuple,
                 albedo3:tuple,
                 lit:bool, 
                 tags:list[str]=None):
        super().__init__(vertices, (0, 0, 0), lit, tags)

        self.albedo1 = albedo1
        self.albedo2 = albedo2
        self.albedo3 = albedo3

    def get_albedo1(self):
        return self.albedo1
    
    def get_albedo1(self, albedo1:tuple):
        self.albedo1 = albedo1

    def get_albedo2(self):
        return self.albedo2
    
    def get_albedo2(self, albedo2:tuple):
        self.albedo1 = albedo2

    def get_albedo3(self):
        return self.albedo3
    
    def get_albedo3(self, albedo3:tuple):
        self.albedo1 = albedo3



class Mesh(Abstract):
    def __init__(self, 
                 name:str=None,
                 location:Matrix=None, 
                 distortion:Matrix=None, 
                 tags:list[str]=None,
                 script=None,
                 parent=None, 
                 children=None):
        super().__init__(name, location, distortion, tags, script, parent, children)
    
    def change_tris_to_gradient(self, colour1, colour2, colour3):
        for tri in self.get_substracts_of_type(Tri):
            self.add_child_relative(GradientTri(tri.vertices.get_transpose().get_contents(), colour1, colour2, colour3, tri.lit))
            tri.kill_self_and_substracts()
            del tri
    
    def change_tris_to_flat_colour(self, colour):
        for tri in self.get_substracts_of_type(GradientTri):
            self.add_child_relative(Tri(tri.vertices.get_transpose().get_contents(), colour, tri.lit))
            tri.kill_self_and_substracts()
            del tri


class Plane(Mesh):
    def __init__(self, 
                 name:str, 
                 quadResolution:tuple,
                 colour:tuple, 
                 lit:bool=None,
                 location:Matrix=None, 
                 distortion:Matrix=None,
                 tags:list[str]=None,
                 script=None):
        super().__init__(name, 
                         location if location else ORIGIN, 
                         distortion if distortion else I3,
                         tags if tags else [],
                         script)
        self.quadResolution = quadResolution # Number of quads along each side
        self.colour = colour
        self.lit = lit if lit is not None else False

        self.generate_plane()

    def generate_plane(self):
        quadWidth = 1 / self.quadResolution[0]
        quadHeight = 1 / self.quadResolution[1]

        for i in range(self.quadResolution[0]):
            for j in range(self.quadResolution[1]):
                corner = (-0.5 + quadWidth * i, -0.5 + quadHeight * j)

                self.add_child_relative(Tri([[corner[0], 0, corner[1]],
                                             [corner[0], 0, corner[1] + quadHeight],
                                             [corner[0] + quadWidth, 0, corner[1]]], self.colour, self.lit, ["PlaneTri"]))
                self.add_child_relative(Tri([[corner[0] + quadWidth, 0, corner[1] + quadHeight],
                                             [corner[0], 0, corner[1] + quadHeight],
                                             [corner[0] + quadWidth, 0, corner[1]]], self.colour, self.lit, ["PlaneTri"]))
        
    def set_quad_resolution(self, quadResolution:tuple):
        tris = self.get_children_with_tag("PlaneTri")
        for tri in tris:
            tri.kill_self()
        
        self.quadResolution = quadResolution

        self.generate_plane()

    def set_pattern_triangles(self, colour1:tuple, colour2:tuple):
        tris = self.get_children_with_tag("PlaneTri")

        for i in range(0, len(tris), 2):
            tris[i].set_albedo(colour1)
            tris[i+1].set_albedo(colour2)

    def set_pattern_gradient(self, left, right):
        tris = self.get_children_with_tag("PlaneTri")

        step = []

        for i in range(3):
            step.append((left[i] - right[i]) / self.quadResolution[1])

        for i in range(self.quadResolution[1]):
            for j in range(self.quadResolution[1] * 2):
                tris[i * self.quadResolution[1] + j].set_albedo((left[0] + j * step[0], left[1] + j * step[1], left[2] + j * step[2]))



class Cube(Mesh):
    def __init__(self, 
                 name:str, 
                 colour:tuple, 
                 lit:bool=None,
                 location:Matrix=None, 
                 distortion:Matrix=None,
                 tags:list[str]=None,
                 script=None):
        super().__init__(name, 
                         location if location else ORIGIN, 
                         distortion if distortion else I3,
                         tags if tags else [],
                         script)
        self.colour = colour
        self.lit = lit if lit is not None else False

        self.generate_cube()

    def generate_cube(self):
        # Front
        self.add_child_relative(Tri([[-0.5,-0.5,-0.5],
                                     [-0.5,0.5,-0.5],
                                     [0.5,-0.5,-0.5]], self.colour, self.lit))
        self.add_child_relative(Tri([[0.5,0.5,-0.5],
                                     [-0.5,0.5,-0.5],
                                     [0.5,-0.5,-0.5]], self.colour, self.lit))
        # Back
        self.add_child_relative(Tri([[0.5,0.5,0.5],
                                     [-0.5,0.5,0.5],
                                     [0.5,-0.5,0.5]], self.colour, self.lit))
        self.add_child_relative(Tri([[-0.5,-0.5,0.5],
                                     [-0.5,0.5,0.5],
                                     [0.5,-0.5,0.5]], self.colour, self.lit))
        # Left
        self.add_child_relative(Tri([[-0.5,-0.5,0.5],
                                     [-0.5,0.5,0.5],
                                     [-0.5,-0.5,-0.5]], self.colour, self.lit))
        self.add_child_relative(Tri([[-0.5,0.5,-0.5],
                                     [-0.5,0.5,0.5],
                                     [-0.5,-0.5,-0.5]], self.colour, self.lit))
        # Right
        self.add_child_relative(Tri([[0.5,0.5,-0.5],
                                     [0.5,0.5,0.5],
                                     [0.5,-0.5,-0.5]], self.colour, self.lit))
        self.add_child_relative(Tri([[0.5,-0.5,0.5],
                                     [0.5,0.5,0.5],
                                     [0.5,-0.5,-0.5]], self.colour, self.lit))
        # Top
        self.add_child_relative(Tri([[-0.5,0.5,-0.5],
                                     [-0.5,0.5,0.5],
                                     [0.5,0.5,-0.5]], self.colour, self.lit))
        self.add_child_relative(Tri([[0.5,0.5,0.5],
                                     [-0.5,0.5,0.5],
                                     [0.5,0.5,-0.5]], self.colour, self.lit))
        # Bottom
        self.add_child_relative(Tri([[-0.5,-0.5,-0.5],
                                     [-0.5,-0.5,0.5],
                                     [0.5,-0.5,-0.5]], self.colour, self.lit))
        self.add_child_relative(Tri([[0.5,-0.5,0.5],
                                     [-0.5,-0.5,0.5],
                                     [0.5,-0.5,-0.5]], self.colour, self.lit))


        
class Camera(Abstract):
    def __init__(self, name:str, location, distortion, fieldOfView:float):
        super().__init__(name, location, distortion, ["Camera"])

        self.perspectiveConstant = math.tan((fieldOfView / 180) * math.pi / 2) / (DISPLAY.resolution[1] / 2)
        # This converts the field of view into radians, then finds the perspective
        # constant needed to get that field of view.

        # To figure out this process, let's imagine a tower exactly one unit
        # away from the camera, so we're only dividing by the constant (1 * constant)

        # We can find half the number of units the fov will reach up the tower by taking
        # tan(half the fov), because it makes a right angled triangle and tan(theta) 
        # equals the opposite over the adjacent.

        # Therefore, we know tan(theta) / perspectiveConstant = 1/2 the resolution

        # Rearrange to make perspectiveConstant = tan(theta) / half the resolution
        
    def project_tri(self, cameraLocationMatrix:Matrix, inversion:Matrix, tri, depthBuffer, lights:list[Abstract]=None):
        triLocation = tri.objectiveLocation.get_contents()

        triLocationMatrix = Matrix([[triLocation[0][0], triLocation[0][0], triLocation[0][0]],  # This is the tri's location
                                    [triLocation[1][0], triLocation[1][0], triLocation[1][0]],  # repeated three times as collumbs
                                    [triLocation[2][0], triLocation[2][0], triLocation[2][0]]]) # in a 3x3 matrix

        triObjectiveVertices = tri.objectiveDistortion.apply(tri.get_vertices()).add(triLocationMatrix) # The tri's vertices in objective space
        
        triCameraVertices = inversion.apply(triObjectiveVertices.subtract(cameraLocationMatrix)).get_contents() # This is the tri's vertices
                                                                                                                # relative to the camera
        # Finds the tri's position relative to the camera
        
        if triCameraVertices[2][0] > 0.1 and triCameraVertices[2][1] > 0.1 and triCameraVertices[2][2] > 0.1:
            # Culls all tris behind the camera

            if tri.lit and lights: # Calculates normal and changes brightness accordingly
                pass
            
            displaySizeX = DISPLAY.resolution[0] / 2
            displaySizeY = DISPLAY.resolution[1] / 2

            vertex1 = (math.floor(triCameraVertices[0][0] / (triCameraVertices[2][0] * self.perspectiveConstant) + displaySizeX), 
                       math.floor(-triCameraVertices[1][0] / (triCameraVertices[2][0] * self.perspectiveConstant) + displaySizeY))
            
            vertex2 = (math.floor(triCameraVertices[0][1] / (triCameraVertices[2][1] * self.perspectiveConstant) + displaySizeX), 
                       math.floor(-triCameraVertices[1][1] / (triCameraVertices[2][1] * self.perspectiveConstant) + displaySizeY))
            
            vertex3 = (math.floor(triCameraVertices[0][2] / (triCameraVertices[2][2] * self.perspectiveConstant) + displaySizeX), 
                       math.floor(-triCameraVertices[1][2] / (triCameraVertices[2][2] * self.perspectiveConstant) + displaySizeY))

            if type(tri) == GradientTri:
                DISPLAY.draw_coloured_triangle(vertex1, vertex2, vertex3, 
                                               depthBuffer, triCameraVertices[2][0], triCameraVertices[2][1], triCameraVertices[2][2],
                                               tri.albedo1, tri.albedo2, tri.albedo3)

            else:
                DISPLAY.draw_coloured_triangle(vertex1, vertex2, vertex3, 
                                               depthBuffer, triCameraVertices[2][0], triCameraVertices[2][1], triCameraVertices[2][2],
                                               tri.albedo)
                
            #pygame.draw.polygon(window, tri.albedo, screenSpaceCoordinates)
        
        
        
    def rasterize(self):
        tris = ROOT.get_substracts_of_type(Tri) + ROOT.get_substracts_of_type(GradientTri)
        
        inversion = self.objectiveDistortion.get_3x3_inverse()
        location = self.objectiveLocation.get_contents()
        locationMatrix = Matrix([[location[0][0], location[0][0], location[0][0]],
                                 [location[1][0], location[1][0], location[1][0]],
                                 [location[2][0], location[2][0], location[2][0]]])
        
        DISPLAY.fill((255, 255, 255))
        DEPTHBUFFER.fill(1024.0)
        
        for tri in tris:
            self.project_tri(locationMatrix, inversion, tri, DEPTHBUFFER)

        DISPLAY.render_image(window)
        #DEPTHBUFFER.render_depthbuffer(window, (0, 0))



    def render(self):
        self.rasterize()

        #window.blit(depthBuffer, (0, 0))



# ---------------- GUI OBJECTS ----------------

# Some theme constants:

EDITORCOLOUR = (108, 108, 108)
EDITORDARK = (0, 0, 0)
EDITORHIGHLIGHT = (255, 255, 255)

EDITORFONT = pygame.font.Font("freesansbold.ttf", 24)



class EditorPanel:
    def __init__(self, size:tuple, location:tuple, colour:tuple, subelements:list):
        self.size = size
        self.location = location

        self.colour = colour

        print(size)

        self.surface = pygame.Surface(size)
        self.surface.fill(colour)

        self.subelements = subelements
        
    def get_surface_colour(self):
        return self.colour
    
    def set_surface_colour(self, colour):
        self.colour = colour
        self.surface.fill(colour)

    def get_title(self):
        return self.title
    
    def set_title(self, title):
        self.title = title

    def render(self):
        window.blit(self.surface, self.location)
    
    def process(self, mousePosition):
        print(f"Rendering Editorpanel")
        self.render()

        for element in self.subelements:
            element.process()
        
        

class Text(EditorPanel):
    def __init__(self, size:tuple, location:tuple, colour:tuple, text:str, textColour:tuple, subelements:list):
        super().__init__(size, location, colour, subelements)
        
        self.textColour = textColour
        self.text = text
        self.rasterisedText = EDITORFONT.render(text, False, textColour)

    def get_text(self):
        return self.text
        
    def set_text(self, text):
        self.text = text
        self.rasterisedText = EDITORFONT.render(text, False, self.textColour)
        
    def get_text_colour(self):
        return self.textColour
    
    def set_text_colour(self, textColour):
        self.textColour = textColour
        self.rasterisedText = EDITORFONT.render(self.text, False, textColour)
        
    def render(self):
        super().render()
        window.blit(self.rasterisedText, self.location)
        
        
            
class Button(Text):
    def __init__(self, size:tuple, location:tuple, colour:tuple, text:str, textColour:tuple, subelements:list):
        super().__init__(size, location, colour, text, textColour, subelements)
        
    def press_action(self):
        pass
    
    def check_for_mouse(self, mousePosition):
        if self.surface.get_rect(topleft=self.location).collidepoint(mousePosition):
            if pygame.mouse.get_pressed()[0]:
                self.set_surface_colour(EDITORCOLOUR)
                self.set_text_colour(EDITORDARK)
                
                self.press_action()
            else:
                self.set_surface_colour(EDITORHIGHLIGHT)
                self.set_text_colour(EDITORDARK)
        else:
            self.set_surface_colour(EDITORCOLOUR)
            self.set_text_colour(EDITORHIGHLIGHT)
            
    def process(self, mousePosition):
        self.check_for_mouse(mousePosition)
        self.render()
        
class ClickActionMenu(EditorPanel):
    def __init__(self, location:tuple, subelements:list[Button]):
        super().__init__((100, len(subelements) * 28 + 2), location, EDITORCOLOUR, subelements)

        self.enabled = False

        count = 0
        for button in subelements:
            button.location = (location[0], location[1] + (count * 28) + 4)
            count += 1

    def process(self, mousePosition):
        if self.enabled:
            print(f"ClickActionMenu is enabled.")
            self.render()

            for button in self.buttons:
                button.process(mousePosition)

    def toggle(self):
        self.enabled = not self.enabled

class ButtonBar(EditorPanel):
    def __init__(self, size:tuple, location:tuple, colour:tuple, subelements:list[Button], buttonSpacing:int):
        super().__init__(size, location, colour, subelements)

        count = 0
        for button in subelements:
            button.location = (location[0] + (count * (buttonSpacing + 2)) + 2, location[1] + 2)
            count += 1
        
    def process(self, mousePosition):
        print(super())
        super().render()

        print(self.location)

        for button in self.subelements:
            print(button.text)
            print(button.location)
            button.process(mousePosition)
            
            

# Top Menu Bar buttons
class ExitButton(Button):
    def __init__(self):
        super().__init__((26, 100), (0, 0), EDITORCOLOUR, "Exit", EDITORHIGHLIGHT, [])
    
class FileButtonClickActionMenu(ClickActionMenu):
    def __init__(self):
        super().__init__(((2, 28) [ExitButton()]))

class FileButton(Button):
    def __init__(self):
        super().__init__((70, 26), (2, 2), EDITORCOLOUR, "File", EDITORHIGHLIGHT, [FileButtonClickActionMenu])

    def press_action(self):
        print("Pressed!")
        self.subelements[0].toggle()

class TopMenuBar(ButtonBar):
    def __init__(self):
        super().__init__((SCREENSIZE[0], 30), 
                         (0, 0), 
                         EDITORDARK, 
                         [FileButton(),
                         Button((70, 26), (74, 2), EDITORCOLOUR, "Edit", EDITORHIGHLIGHT, []),
                         Button((70, 26), (146, 2), EDITORCOLOUR, "Play", EDITORHIGHLIGHT, [])], 
                         70)
        

# GUI setup

guiElements = [TopMenuBar()]



# ---------------- SCENE INITIALISATION ----------------




# ---------------- MAIN LOOP ----------------

def initialise_scene_editmode():
        
    origin = Abstract("Origin")
    ROOT.add_child_relative(origin)

    origin.attach_script("/project/scripts/hello.py")

    environment = Abstract("Environment")
    origin.add_child_relative(environment)

    player = Abstract("Player", Matrix([[0],
                                        [0],
                                        [-4]]))
    origin.add_child_relative(player)

    camera = Camera("Camera", Matrix([[0],
                                    [0],
                                    [0]]), I3, 60)
    player.add_child_relative(camera)

    camera.attach_script()

    cube = Cube("Cube", (200, 200, 200), True)
    environment.add_child_relative(cube)

    cube.change_tris_to_gradient((248, 54, 119), (58, 244, 189), (229, 249, 54))

    leftWall = Plane("LeftWall", (4, 4), (0, 0, 0), True, Matrix([[-2],
                                                                [1],
                                                                [0]]), Matrix([[0, 4, 0],
                                                                                [-4, 0, 0],
                                                                                [0, 0, 4]]))
    environment.add_child_relative(leftWall)

    backWall = Plane("BackWall", (4, 4), (0, 0, 0), True, Matrix([[0],
                                                            [1],
                                                            [2]]), Matrix([[4, 0, 0],
                                                                        [0, 0, 4],
                                                                        [0, -4, 0]]))
    environment.add_child_relative(backWall)

    floor = Plane("Ground", (4, 4), (0, 0, 0), True, Matrix([[0],
                                                            [-1],
                                                            [0]]), Matrix([[4, 0, 0],
                                                                        [0, 4, 0],
                                                                        [0, 0, 4]]))
    environment.add_child_relative(floor) 

    floor.set_pattern_triangles((0, 0, 0), (108, 108, 108))
    backWall.set_pattern_triangles((0, 0, 0), (108, 108, 108))
    leftWall.set_pattern_triangles((252, 252, 252), (108, 108, 108))

    environment.set_distortion_objective(Matrix([[1, 0, 0],
                                                [0, 1, 0],
                                                [0, 0, 1]]))

def game_loop_editmode(delta:float):
    ROOT.process()

    events = pygame.event.get()
    
    for event in events:
        if event.type == pygame.QUIT:
            engineRunning = False
    
    '''q`   AVF
    playerMovement = [[0],
                      [0],
                      [0]]
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        playerMovement[2] = [1]
    if keys[pygame.K_s]:
        playerMovement[2] = [-1]
    if keys[pygame.K_a]:
        playerMovement[0] = [-1]
    if keys[pygame.K_d]:
        playerMovement[0] = [1]

    player.translate_relative(Matrix(playerMovement).set_magnitude(movementSpeed * frameDelta))
        
    if keys[pygame.K_RIGHT]:
        player.rotate_euler_radians(0, lookSpeed * frameDelta, 0)
    if keys[pygame.K_LEFT]:
        player.rotate_euler_radians(0, -lookSpeed * frameDelta, 0)

    if keys[pygame.K_UP]:
        camera.rotate_euler_radians(-lookSpeed * frameDelta, 0, 0)
    if keys[pygame.K_DOWN]:
        camera.rotate_euler_radians(lookSpeed * frameDelta, 0, 0)

    cube.rotate_euler_radians(frameDelta, frameDelta, 0)
        
    window.fill((255, 255, 255))

    camera.render()
    '''

    mousePosition = pygame.mouse.get_pos()
    
    for panel in guiElements:
        panel.process(mousePosition)
        
    pygame.display.flip()

def initialise_scene_playmode():
    pass

def game_loop_playmode(delta:float):
    pass


movementSpeed = 4
lookSpeed = 2

frameDelta = 0

while engineRunning:
    startTime = time.time()

    game_loop_editmode(frameDelta)
        
    frameDelta = time.time() - startTime

    if frameDelta > 0.1:
        print("Framedrop detected")

    try:
        print(f"Finished frame in {frameDelta} seconds. \nEquivalent to {1 / (frameDelta)} Hz \n")
    except:
        print("Very fast")