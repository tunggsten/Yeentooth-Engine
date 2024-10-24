import pygame
import math


# ---------------- MATHEMATICAL CONSTRUCTS ----------------

def clamp(val:float, min:float, max:float): # the math library didn't have a function to do this so 
    if val > max:                           # have to pick up their slack
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
    
    def add_child_relative(self, newChild):
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
        

                            
# Important default abstracts:

ROOT = Abstract("Root")

    

# ---------------- GRAPHICS OBJECTS ----------------

# Pygame Setup - initialises the window

# I'm doing this here because some of the graphics abstracts
# have to reference these

pygame.init()
SCREENSIZE = (640, 480)
SCREENSIZEFROMCENTER = (SCREENSIZE[0] / 2, SCREENSIZE[1] / 2)
window = pygame.display.set_mode(SCREENSIZE)
pygame.display.set_caption("yeentooth")
clock = pygame.time.Clock()
running = True



class Texture(): # This is here so I don't have to make a copy of a
                 # surface for every triangle it's mapped to
    def __init__(self, texturePath):
        self.surface = pygame.image.load(texturePath)
    
    def get_colour_at(self, index:tuple):
        return self.surface.get_at(index)



class Image(): # This is like a shitty fake version of pygame.Surface
    def __init__(self, resolution:tuple, pixelSize:tuple, colorspace:bool):
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
    
    def interpolate_coordinate(self, coordinate1:tuple, coordinate2:tuple, t:float):
        return (math.floor(coordinate1[0] + (coordinate2[0] - coordinate1[0]) * abs(t)),
                math.floor(coordinate1[1] + (coordinate2[1] - coordinate1[1]) * abs(t)))
    
    

    def draw_horizontal_line(self, 
                             x1:int, 
                             x2:int, 
                             y:int,
                             depthBuffer, 
                             depth1:float,
                             depth2:float, 
                             colour1:tuple=None, 
                             colour2:tuple=None,
                             **kwargs):
        texture = kwargs.get("texture", None) 

        uv1 = kwargs.get("uv1", None)
        uv2 = kwargs.get("uv2", None)

        if 0 <= y < self.resolution[1]:
            lineLength = abs(x2 - x1)
            for i in range(x1, x2, 1 if x1 < x2 else -1):
                if 0 <= i < self.resolution[0]:
                    interpolationAmount = (i - x1) / lineLength
                    depth = self.interpolate_value(depth1, depth2, interpolationAmount)
                    
                    if depth <= depthBuffer.contents[y][i]:
                        if colour2:
                            pixelColour = self.interpolate_colour(colour1, colour2, interpolationAmount)
                            self.contents[y][i] = pixelColour
                            depthBuffer.contents[y][i] = depth
                        elif texture:
                            self.contents[y][i] = texture.get_colour_at(self.interpolate_coordinate(uv1, uv2, interpolationAmount))
                            depthBuffer.contents[y][i] = depth
                        else:
                            self.contents[y][i] = colour1
                            depthBuffer.contents[y][i] = depth
                            
                            

    def draw_flat_based_triangle(self, 
                                 bottomLeft:tuple, 
                                 bottomRight:tuple, 
                                 point:tuple, 
                                 depthBuffer,
                                 depth1:float,
                                 depth2:float,
                                 depth3:float,
                                 colour1:tuple=None, 
                                 colour2:tuple=None, 
                                 colour3:tuple=None,
                                 **kwargs):
        texture = kwargs.get("texture", None) 

        uv1 = kwargs.get("uv1", None)
        uv2 = kwargs.get("uv2", None)
        uv3 = kwargs.get("uv3", None)

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
                self.draw_horizontal_line(left, right, y, depthBuffer, leftDepth, rightDepth, 
                                        self.interpolate_colour(colour1, colour3, amountDone), 
                                        self.interpolate_colour(colour2, colour3, amountDone))
                
            elif texture:
                self.draw_horizontal_line(left, right, y, depthBuffer, leftDepth, rightDepth,
                                          texture=texture,
                                          uv1=self.interpolate_coordinate(uv1, uv3, amountDone),
                                          uv2=self.interpolate_coordinate(uv2, uv3, amountDone))
            else:
                self.draw_horizontal_line(left, right, y, depthBuffer, leftDepth, rightDepth, colour1)
                
                

    def draw_triangle(self, 
                      vertex1:tuple,
                      vertex2:tuple,
                      vertex3:tuple,
                      depthBuffer,
                      depth1:float,
                      depth2:float,
                      depth3:float,
                      colour1:tuple=None,
                      colour2:tuple=None,
                      colour3:tuple=None,
                      **kwargs):
        
        texture = kwargs.get("texture", None) 

        uv1 = kwargs.get("uv1", None)
        uv2 = kwargs.get("uv2", None)
        uv3 = kwargs.get("uv3", None)

        # Find the middle vertex
        heights = [vertex1[1], vertex2[1], vertex3[1]]

        # Believe it or not, this is a sorting algorithm.
        if heights[0] > heights[1]:
            if heights[0] > heights[2]:
                if heights[1] > heights[2]:
                    vertices = [vertex1, vertex2, vertex3]
                    colours = [colour1, colour2, colour3]
                    depths = [depth1, depth2, depth3]
                    uvs = [uv1, uv2, uv3]
                else:
                    vertices = [vertex1, vertex3, vertex2]
                    colours = [colour1, colour3, colour2]
                    depths = [depth1, depth3, depth2]
                    uvs = [uv1, uv3, uv2]
            else:
                vertices = [vertex3, vertex1, vertex2]
                colours = [colour3, colour1, colour2]
                depths = [depth3, depth1, depth2]
                uvs = [uv3, uv1, uv2]
        else:
            if heights[0] < heights[2]:
                if heights[1] < heights[2]:
                    vertices = [vertex3, vertex2, vertex1]
                    colours = [colour3, colour2, colour1]
                    depths = [depth3, depth2, depth1]
                    uvs = [uv3, uv2, uv1]
                else:
                    vertices = [vertex2, vertex3, vertex1]
                    colours = [colour2, colour3, colour1]
                    depths = [depth2, depth3, depth1]
                    uvs = [uv2, uv3, uv1]
            else:
                vertices = [vertex2, vertex1, vertex3]
                colours = [colour2, colour1, colour3]
                depths = [depth2, depth1, depth3]
                uvs = [uv2, uv1, uv3]

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

            self.draw_flat_based_triangle(vertices[1], sliceCoordinate, vertices[2], 
                                          depthBuffer, depths[1], sliceDepth, depths[2],
                                          colours[1], sliceColour, colours[2])
            self.draw_flat_based_triangle(vertices[1], sliceCoordinate, vertices[0], 
                                          depthBuffer, depths[1], sliceDepth, depths[0],
                                          colours[1], sliceColour, colours[0])
            
        elif texture:
            sliceUV = self.interpolate_coordinate(uvs[0], uvs[2], 1 - sliceAmount)

            self.draw_flat_based_triangle(vertices[1], sliceCoordinate, vertices[2], 
                                          depthBuffer, depths[1], sliceDepth, depths[2],
                                          texture=texture,
                                          uv1=uvs[1], uv2=sliceUV, uv3=uvs[2])
            self.draw_flat_based_triangle(vertices[1], sliceCoordinate, vertices[0], 
                                          depthBuffer, depths[1], sliceDepth, depths[0],
                                          texture=texture,
                                          uv1=uvs[1], uv2=sliceUV, uv3=uvs[0])
            
        else:
            self.draw_flat_based_triangle(vertices[1], sliceCoordinate, vertices[2], 
                                          depthBuffer, depths[1], sliceDepth, depths[2],
                                          colour1)
            self.draw_flat_based_triangle(vertices[1], sliceCoordinate, vertices[0],
                                          depthBuffer, depths[1], sliceDepth, depths[0],
                                          colour1)

    def render_image(self, target:pygame.Surface, position:tuple):
        for row in range(position[1], position[1] + self.resolution[1]):
            for pixel in range(position[0], position[0] + self.resolution[0]):
                pygame.draw.rect(target, 
                                 self.contents[row][pixel], 
                                 pygame.Rect((pixel * self.pixelSize[0], row * self.pixelSize[1]), self.pixelSize))

    def render_depthbuffer(self, target, position):
        for row in range(position[1], position[1] + self.resolution[1]):
            for pixel in range(position[0], position[0] + self.resolution[0]):
                pygame.draw.rect(target, 
                                 (clamp(self.contents[row][pixel] * 25, 0, 255), 
                                  clamp(self.contents[row][pixel] * 25, 0, 255),
                                  clamp(self.contents[row][pixel] * 25, 0, 255)),
                                 pygame.Rect((pixel * self.pixelSize[0], row * self.pixelSize[1]), self.pixelSize))



# This will be the colour display triangles get rendered to

DISPLAY = Image((128, 96), (5, 5), True)

displaySizeX = DISPLAY.resolution[0] / 2
displaySizeY = DISPLAY.resolution[1] / 2

# This stores the depth information of the scene, so we can
# check if a pixel should be behind another pixel already rendered.
DEPTHBUFFER = Image((128, 96), (5, 5), False)



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



class TextureTri(Tri): # Tri with a texture
    def __init__(self,
                 vertices:list[list[float]], 
                 texture:Texture,
                 uv1:tuple,
                 uv2:tuple,
                 uv3:tuple,
                 lit:bool, 
                 tags:list[str]=None):
        super().__init__(vertices, (0, 0, 0), lit, tags)

        self.texture = texture

        self.uv1 = uv1
        self.uv2 = uv2
        self.uv3 = uv3



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
        for tri in self.get_substracts_of_type(Tri) + self.get_substracts_of_type(TextureTri):
            print(tri)
            self.add_child_relative(GradientTri(tri.vertices.get_transpose().get_contents(), colour1, colour2, colour3, tri.lit, tri.tags))
            tri.kill_self_and_substracts()
            del tri
    
    def change_tris_to_flat_colour(self, colour):
        for tri in self.get_substracts_of_type(GradientTri) + self.get_substracts_of_type(TextureTri):
            self.add_child_relative(Tri(tri.vertices.get_transpose().get_contents(), colour, tri.lit, tri.tags))
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
            for j in range(self.quadResolution[0] * 2):
                tris[i * self.quadResolution[0] * 2 + j].set_albedo((left[0] + j * step[0], 
                                                                 left[1] + j * step[1], 
                                                                 left[2] + j * step[2]))
    
    def set_pattern_texture(self, texture:Texture):
        textureHeight = texture.surface.get_height() - 1

        UVWidth = math.floor((texture.surface.get_width() - 1)/ self.quadResolution[0])
        UVHeight = math.floor((textureHeight - 1) / self.quadResolution[1]) 

        tris = self.get_children_with_tag("PlaneTri")

        for i in range(self.quadResolution[1]):
            for j in range(0, self.quadResolution[0] * 2, 2):
                currentTri = tris[i * self.quadResolution[0] * 2 + j]

                self.add_child_relative(TextureTri(currentTri.vertices.get_transpose().get_contents(), texture, 
                                                   (i * UVWidth, textureHeight - (j/2) * UVHeight),
                                                   (i * UVWidth, textureHeight - ((j/2)+1) * UVHeight),
                                                   ((i+1) * UVWidth, textureHeight - (j/2) * UVHeight), True))
                
                currentTri = tris[i * self.quadResolution[0] * 2 + j + 1]

                self.add_child_relative(TextureTri(currentTri.vertices.get_transpose().get_contents(), texture, 
                                                   ((i+1) * UVWidth, textureHeight - (j/2 + 1) * UVHeight),
                                                   (i * UVWidth, textureHeight - ((j/2)+1) * UVHeight),
                                                   ((i+1) * UVWidth, textureHeight - (j/2) * UVHeight), True))
        
        for tri in tris:
            tri.kill_self_and_substracts()



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
                                     [0.5,-0.5,-0.5]], self.colour, self.lit, ["CubeTri"]))
        self.add_child_relative(Tri([[0.5,0.5,-0.5],
                                     [-0.5,0.5,-0.5],
                                     [0.5,-0.5,-0.5]], self.colour, self.lit, ["CubeTri"]))
        # Back
        self.add_child_relative(Tri([[0.5,0.5,0.5],
                                     [-0.5,0.5,0.5],
                                     [0.5,-0.5,0.5]], self.colour, self.lit, ["CubeTri"]))
        self.add_child_relative(Tri([[-0.5,-0.5,0.5],
                                     [-0.5,0.5,0.5],
                                     [0.5,-0.5,0.5]], self.colour, self.lit, ["CubeTri"]))
        # Left
        self.add_child_relative(Tri([[-0.5,-0.5,0.5],
                                     [-0.5,0.5,0.5],
                                     [-0.5,-0.5,-0.5]], self.colour, self.lit, ["CubeTri"]))
        self.add_child_relative(Tri([[-0.5,0.5,-0.5],
                                     [-0.5,0.5,0.5],
                                     [-0.5,-0.5,-0.5]], self.colour, self.lit, ["CubeTri"]))
        # Right
        self.add_child_relative(Tri([[0.5,0.5,-0.5],
                                     [0.5,0.5,0.5],
                                     [0.5,-0.5,-0.5]], self.colour, self.lit, ["CubeTri"]))
        self.add_child_relative(Tri([[0.5,-0.5,0.5],
                                     [0.5,0.5,0.5],
                                     [0.5,-0.5,-0.5]], self.colour, self.lit, ["CubeTri"]))
        # Top
        self.add_child_relative(Tri([[-0.5,0.5,-0.5],
                                     [-0.5,0.5,0.5],
                                     [0.5,0.5,-0.5]], self.colour, self.lit, ["CubeTri"]))
        self.add_child_relative(Tri([[0.5,0.5,0.5],
                                     [-0.5,0.5,0.5],
                                     [0.5,0.5,-0.5]], self.colour, self.lit, ["CubeTri"]))
        # Bottom
        self.add_child_relative(Tri([[-0.5,-0.5,-0.5],
                                     [-0.5,-0.5,0.5],
                                     [0.5,-0.5,-0.5]], self.colour, self.lit, ["CubeTri"]))
        self.add_child_relative(Tri([[0.5,-0.5,0.5],
                                     [-0.5,-0.5,0.5],
                                     [0.5,-0.5,-0.5]], self.colour, self.lit, ["CubeTri"]))
        
    def set_pattern_texture(self, texture:Texture):
        textureSize = texture.surface.get_size()

        tris = self.get_children_with_tag("CubeTri")
        print(self.get_children())
        print(tris)

        for i in range(6):
            self.add_child_relative(TextureTri(tris[i * 2].get_vertices().get_transpose().get_contents(),
                                               texture,
                                               (0, 0), 
                                               (textureSize[0] - 1, 0), 
                                               (0, textureSize[1] - 1), True))
            
            self.add_child_relative(TextureTri(tris[i * 2 + 1].get_vertices().get_transpose().get_contents(),
                                               texture,
                                               (textureSize[0] - 1, textureSize[1] - 1), 
                                               (textureSize[0] - 1, 0), 
                                               (0, textureSize[1] - 1), True))
            
        for tri in tris:
            tri.kill_self_and_substracts()



class Wavefront(Mesh):
    def __init__(self, 
                 name:str, 
                 obj:str,
                 colour:tuple, 
                 lit:bool=None,
                 location:Matrix=None, 
                 distortion:Matrix=None,
                 tags:list[str]=None,
                 script=None,
                 **kwargs):
        
        super().__init__(name, 
                         location if location else ORIGIN, 
                         distortion if distortion else I3,
                         tags if tags else [],
                         script)
        
        self.obj = obj # Beware! This only works if your Wavefront file
                       # is split into triangles. No quads! Especially no n-gons.

                       # Don't even think about adding vertex normals in there.

        self.texture = kwargs.get("texture", None)

        self.colour = colour
        self.lit = lit if lit is not None else False

        self.generate_mesh(self.obj)

    def generate_mesh(self, obj):
        vertices = []
        uvs = []

        if self.texture:
            textureSize = (self.texture.surface.get_width() - 1,
                           self.texture.surface.get_height() - 1)

        with open(obj, "r") as obj:

            for line in obj:
                if line[0] == "v": # This could be "v" (vertex) or "vt" (texture coordinate)
                                   # so we have to check the second character too.
                    if line[1] == "t": # This means it's a UV coordinate.
                        values = line.split()
                        uvs.append([float(values[1]), float(values[2])])

                    elif line[1] == " ": # We still have to check cause it could also be "vn" or "vp",
                                         # but this means it's a vertex.
                        values = line.split()
                        vertices.append([float(values[1]), float(values[2]), float(values[3])])

                elif line[0] == "f": # If the file's defining a face:

                    # Here the line is gonna be giving us three verteces 
                    # and three uvs in the format vertex1/uv1 v2/uv2 v3/v3,
                    # so we have to split each element in valuses again.

                    # Each one is a one-based index to a vertex or uv defined
                    # earlier in the file.

                    values = line.split()

                    v = []
                    vt = []

                    for i in range(1, 4):
                        indexes = values[i].split("/")
                        print(f"Indexes: {indexes}")
                        v.append(vertices[int(indexes[0]) - 1])

                        try: # Sometimes you won't have UVs so we have to account for it
                            print(f"Appending UV: {uvs[int(indexes[1]) - 1]}")

                            # This is carcinogenic but we have to do this because
                            # wavefront files store uvs with coordinates between
                            # 1 and 0, so we have to scale it by the texture size

                            relativeSpaceUVS = uvs[int(indexes[1]) - 1]
                            textureSpaceUVS = [math.floor(relativeSpaceUVS[0] * textureSize[0]),
                                               textureSize[1] - math.floor(relativeSpaceUVS[1] * textureSize[1])]
                            
                            vt.append(textureSpaceUVS)
                        except:
                            pass

                    # Now we've extracted our values, we can instantiate our tri.
                    if self.texture:
                        self.add_child_relative(TextureTri(v, self.texture, vt[0], vt[1], vt[2], self.lit, ["MeshTri"]))
                    else:
                        self.add_child_relative(Tri(v, self.colour, self.lit, ["MeshTri"]))

                        


        
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

            vertex1 = (math.floor(triCameraVertices[0][0] / (triCameraVertices[2][0] * self.perspectiveConstant) + displaySizeX), 
                       math.floor(-triCameraVertices[1][0] / (triCameraVertices[2][0] * self.perspectiveConstant) + displaySizeY))
            
            vertex2 = (math.floor(triCameraVertices[0][1] / (triCameraVertices[2][1] * self.perspectiveConstant) + displaySizeX), 
                       math.floor(-triCameraVertices[1][1] / (triCameraVertices[2][1] * self.perspectiveConstant) + displaySizeY))
            
            vertex3 = (math.floor(triCameraVertices[0][2] / (triCameraVertices[2][2] * self.perspectiveConstant) + displaySizeX), 
                       math.floor(-triCameraVertices[1][2] / (triCameraVertices[2][2] * self.perspectiveConstant) + displaySizeY))

            if ((0 <= vertex1[0] <= displaySizeX * 2 - 1 and # This is the worst way i could possibly do this.
                0 <= vertex1[1] <= displaySizeY * 2 - 1) or   # Too bad! It works so it's staying
                (0 <= vertex2[0] <= displaySizeX * 2 - 1 and
                0 <= vertex2[1] <= displaySizeY * 2 - 1) or 
                (0 <= vertex3[0] <= displaySizeX * 2 - 1 and
                0 <= vertex3[1] <= displaySizeY * 2 - 1)):
                
                if type(tri) == GradientTri:
                    DISPLAY.draw_triangle(vertex1, vertex2, vertex3, 
                                          depthBuffer, triCameraVertices[2][0], triCameraVertices[2][1], triCameraVertices[2][2],
                                          tri.albedo1, tri.albedo2, tri.albedo3)
                    
                elif type(tri) == TextureTri:
                    DISPLAY.draw_triangle(vertex1, vertex2, vertex3,
                                          depthBuffer, triCameraVertices[2][0], triCameraVertices[2][1], triCameraVertices[2][2],
                                          texture=tri.texture,
                                          uv1=tri.uv1, uv2=tri.uv2, uv3=tri.uv3)

                else:
                    DISPLAY.draw_triangle(vertex1, vertex2, vertex3, 
                                          depthBuffer, triCameraVertices[2][0], triCameraVertices[2][1], triCameraVertices[2][2],
                                          tri.albedo)
                    
            #pygame.draw.polygon(window, tri.albedo, screenSpaceCoordinates)
        
        
        
    def rasterize(self):
        tris = ROOT.get_substracts_of_type(Tri) + ROOT.get_substracts_of_type(GradientTri) + ROOT.get_substracts_of_type(TextureTri)
        
        inversion = self.objectiveDistortion.get_3x3_inverse()
        location = self.objectiveLocation.get_contents()
        locationMatrix = Matrix([[location[0][0], location[0][0], location[0][0]],
                                 [location[1][0], location[1][0], location[1][0]],
                                 [location[2][0], location[2][0], location[2][0]]])
        
        DISPLAY.fill((255, 255, 255))
        DEPTHBUFFER.fill(1024.0)
        
        for tri in tris:
            self.project_tri(locationMatrix, inversion, tri, DEPTHBUFFER)

        DISPLAY.render_image(window, (0, 0))



    def render(self):
        self.rasterize()

        #window.blit(depthBuffer, (0, 0))



# ---------------- PHYSICS OBJECTS ----------------

# I'm probably not going to finish these but they're here if I or 
# someone else wants to add them in the future.



# Since units are important here, let's establish some conventions:

UNITSCALE = 1 # This is how many meters one unit is equivalent to.

              # I'm doing this 'cause lots of engines let you change it.

              # Like imagine building a mech sim, but you have to keep the physics
              # engine to scale, so your player mesh ends up being 400 units tall.

              # Not ideal.

              # You can change this if you want, but for most things you can just keep
              # it at 1.

STEPSCALE = 1 # This is how many simulated seconds one second at runtime is equivalent to.
              # It's here for the same reasons as UNITSCALE

GRAVFIELDSTRENGTH = 9.81 # The strength of the scene's gravitational field 
                         # measured in Newtons per kilogram (NKg^-1)

                         # It's also the acceleration things will fall at in meters per second per second (ms^-2)

                         # It's named like a constant but you're free to change it if you want

class Body(Abstract):
    def __init__(self, name:str, location:Matrix, velocity:Matrix, angularVelocity:Matrix, mass:float, dynamic:bool=None):
        super().__init__(name, location)
        
        self.velocity = velocity # A 3D collumb vector measured in meters per second (ms^-1)
        self.angularVelocity = angularVelocity
        self.mass = mass # Mass in kilograms (Kg)

        self.dynamic = dynamic if dynamic else True

    def process(self):
        pass
