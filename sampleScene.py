from yeentooth import *
import time


origin = Abstract("Origin")
ROOT.add_child_relative(origin)

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

jonkler = Texture("jonkler.png")

cube = Cube("Cube", (200, 200, 200), True)
environment.add_child_relative(cube)

cube.change_tris_to_gradient((248, 54, 119), (58, 244, 189), (229, 249, 54))


pyramid = Mesh("Pyramid", Matrix([[0],
                                  [0],
                                  [-8]]), I3)
environment.add_child_relative(pyramid)

for i in range(4):
    tri = TextureTri([[0, 1, 0],
                       [-1, -1, 1],
                       [1, -1, 1]], jonkler, (354, 0), (705, 609), (0, 609), True)
    tri.rotate_euler_radians(0, i * (math.pi / 2), 0)

    pyramid.add_child_relative(tri)


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



# ---------------- MAIN LOOP ----------------

movementSpeed = 4
lookSpeed = 2

frameDelta = 0

while running:
    startTime = time.time()

    events = pygame.event.get()
    
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            
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
        
    frameDelta = time.time() - startTime

    if frameDelta > 0.1:
        print("Framedrop detected")

    try:
        print(f"Finished frame in {frameDelta} seconds. \nEquivalent to {1 / (frameDelta)} Hz \n")
    except:
        print("Very fast")
        
    pygame.display.flip()