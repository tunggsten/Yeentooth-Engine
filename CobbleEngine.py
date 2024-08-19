import pygame
from tkinter import *




# ---------------- MATHEMATICAL OBJECTS ----------------

class Matrix:
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
                                              # Like this: Matrix.multiply_contents(1 / numberYoureDividingBy)
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
        
        return Matrix(transpose)
    
    def get_2x2_determinant(self): # Okay, I know this is really ugly but you can only 
                                   # find determinants for square matrices, and I'm only gonna be
                                   # doing that for 2x2 and 3x3 ones so I might as well reduce the
                                   # conditionals.
        return (self.contents[0][0] * self.contents[1][1]) - (self.contents[0][1] * self.contents[1][0])
    
    def get_2x2_inverse(self): # This just uses the set formula.
        
                               # [ [ a, b ],           =     [ [ d, -b ],
                               #   [ c, d ] ] ^ -1             [ -c, a ] ]
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
        
        workingContents = Matrix(
            [
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
        )
        
        # This makes me want to kill myself. /j
        
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
        if self.order != matrixToAddIdk.order:
            print("These have different orders dumbass you can't add them")
            return None
        
        contentsToAdd = matrixToAddIdk.get_contents()
        
        result = []
        
        for row in range(self.order[0]):
            result.append([])
            
            for collumb in range(self.order[1]):
                result[row].append(self.contents[row][collumb] + contentsToAdd[row][collumb])
        
        return Matrix(result)

    def apply(self, right): # Matrix multiplication isn't commutative, so we have one
                            # on the left, and one on the right.
                
                            # Self is on the left. Can you guess where Right is?

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
        rightContents = right.get_contents # each object every single time idc about 
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
    def __init__(self, location = ORIGIN, distortion = I3, parent = None, children = []):
        self.location = location
        self.distortion = distortion
        # Right, I know you're not going to be happy with this but the Distortion
        # parameter handles both orientation AND scale. Why? Because quaternions
        # scare me and God FORBID I actually research anything new for my research 
        # project
        self.parent = parent
        self.children = children
        
    def get_location(self):
        return self.location
    
    def set_location(self, location):
        self.location = location
        
    def get_distortion(self):
        return self.distortion
    
    def set_distortion(self, distortion):
        self.distortion = distortion
        
    def get_parent(self):
        return self.parent
    
    def set_parent(self, parent): # Alter all of the reparenting functions later to 
        if parent:                # preserve world-space positions
            parent.remove_child(self)
            
        self.parent = parent
        
    def add_child(self, child):
        self.children.append(child)
        
    def remove_child(self, child):
        child.set_parent(self.parent)
        self.children.remove(child)
        self.parent.add_child(child)

    def delete_self(self):
        for child in self.children:
            child.set_parent(self.parent)

        parent.remove_child(self)  

    def delete_self_and_children(self):

        

    def move(self, vector):
        self.location = self.location.add(vector)

    def rotate_euler_radians(euler):
        pass
    
    
    

# ---------------- GRAPHICS OBJECTS ----------------

class Poly(Abstract): # This should be a child to a mesh abstract.
    def __init__(self, vertices, colour):   # Vertices should be an array of n arrays.
                                            # Each array is a coordinate, done in clockwise 
                                            # order if you're looking at the opaque side.

                                            # This gets converted to a 3xn matrix with each
                                            # collumb being a coordinate.

                                            # Is this really annoying? Yes!
                                            # But it makes it easier to apply transformation 
                                            # matrices to polygons so I'll just hate myself later 

        self.vertices = Matrix(vertices).get_transpose()

    def translate_world(self, vector):
        self.location = self.location.add(Matrix(vector))
        
class Camera(Abstract):
    def __init__(self, perspectiveConstant):
        self.perspectiveConstant = perspectiveConstant
        
    def project_tri(self, tri):
        relativeVertices = self.distortion.get_3x3_inverse().apply(
            tri.vertices.add(Matrix([[-self.location[0][0], -self.location[0][0], -self.location[0][0]],
                                     [-self.location[1][0], -self.location[1][0], -self.location[1][0]],
                                     [-self.location[2][0], -self.location[2][0], -self.location[2][0]]]))).get_contents()

            # That was horrible! 

            # Lets look at that step-by-step:

            # First, we subtract the camera's location from the location of each vertex.
            # This gives us their postiions relative to *the camera's location* 
            # (not relative to the camera!!!!!)

            # Next, we apply the *inverse* of the camera's distortion to the matrix we
            # got in the last step.
            # This gives us all the coordinates properly relative to the camera.

            # Then, we get the contents of the result so we can use the values in code.

        projectedCoordinates = []

        for i in range(3):
            projectedCoordinates.append([])


helloWorld = Abstract(
    Matrix([[4],
            [5],
            [-2]]),
    
    Matrix([[0, 1, 0],
            [-1, 0, 0],
            [0, 0, 1]])
    
    )

print(helloWorld)

print(helloWorld.get_location().get_contents())

helloWorld.move(Matrix([[1],
                        [3],
                        [1]]))

print(helloWorld.get_location().get_contents())

# Pygame Setup - initialises the window, 
pygame.init()
window = pygame.display.set_mode((320, 240))
clock = pygame.time.Clock()
running = True