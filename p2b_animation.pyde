#donut is the instanced object, 12 instances created with a for loop
time = 0   # use time to move objects from one frame to the next

x_cam = 0
y_cam = 0
z_cam = 600

x_initial = -350
y_initial = 100
z_initial = 4

x_rot = 0
y_rot = PI/2
z_rot = 0

donut_ypos = -200

state = 0 #0 - walking in and turn, 1 - move camera in, 2 - sit, 3 - eat donuts

donut_count = 0

def setup():
    size (800, 800, P3D)
    #size (800, 800, P3D)
    perspective (60 * PI / 180, 1, 0.1, 1000)  # 60 degree field of view
    global img
    img = loadImage("simpsonsroom.jpg")

    
def draw():
    global time
    time += 0.01

    camera (0, 0, 600, 0, 0, 0, 0,  1, 0)  # position the virtual camera

    background (255, 255, 255)  # clear screen and set background to white
    
    global img
    #background(img)

    # create a directional light source
    ambientLight(50, 50, 50)
    lightSpecular(255, 255, 255)
    directionalLight (100, 100, 100, -0.3, 0.5, -1)
    
    noStroke()
    specular (180, 180, 180)
    shininess (15.0)
    
    if (state == 0):
        walking()
    elif (state == 1):
        if (z_cam > 300):
            global z_cam
            z_cam-=5
        else:
            global state
            state+=1
        camera(0, 0, z_cam, 0, 0, 0, 0, 1, 0)
        standing()
        
    elif (state == 2):
        camera(0, 0, z_cam, 0, 0, 0, 0, 1, 0)
        sitting()
    elif (state == 3):
        camera(0, 0, z_cam, 0, 0, 0, 0, 1, 0)
        eating()
    
    
    #backdrop
    beginShape()
    texture(img)
    vertex(-width/2, -height/2, 0, 0, 0)
    vertex(width/2, -height/2, 0, 1280, 0)
    
    vertex(width/2, -height/2, 0, 1280, 0)
    vertex(width/2, height/2, 0, 1280, 720)
    
    vertex(width/2, height/2, 0, 1280, 720)
    vertex(-width/2, height/2, 0, 0, 720)
    
    vertex(-width/2, height/2, 0, 0, 720)
    vertex(-width/2, -height/2, 0, 0, 0)
    
    endShape()

def walking():
    if (x_initial < 0): #walk to couch
        global x_initial
        x_initial+=1
        pushMatrix()
        translate(x_initial, y_initial, z_initial)
        rotateY(PI/2)
        drawHomer()
        popMatrix()
    else: #turn to face camera
        pushMatrix()
        translate(x_initial, y_initial, z_initial)
        global y_rot
        while (y_rot > 0):
            rotateY(y_rot)
            y_rot-=0.00001
        drawHomer()
        popMatrix()
        global state
        state = 1

def eating():
    pushMatrix()
    translate(x_initial, y_initial, z_initial)

    rotateZ(z_rot)
    rotateY(y_rot)
    drawHomer()
    popMatrix()
    
    global donut_ypos
    donut_ypos+=1
    for i in range(0, 12):
        pushMatrix()
        drawDonut(donut_ypos - i*100)
        popMatrix()
    
    fill(255, 0, 0)
    textSize(24)
    text("Mmmmm... Donuts", -150, -90, 10)
    
def drawDonut(y_loc):
    #y_loc+=1
    if (y_loc >= y_initial):
        y_loc = -200
    else:
        pushMatrix()
        translate(90, y_loc, 0)
        rotateZ(PI/2)
    
        #top of donut
        fill(255, 105, 180)
        pushMatrix()
        scale(2.5, 1, 2.5)
        translate(0, -2, 0)
        sphereDetail(60)
        sphere(8)
        popMatrix()
    
        #bottom of donut
        fill(240, 220, 130)
        pushMatrix()
        scale(2.5, 1, 2.5)
        sphereDetail(60)
        sphere(8)
        popMatrix()
    
        popMatrix()
    
def sitting():
    global y_initial, z_rot, y_rot
    
    if (state == 2 and y_initial > 50):
        pushMatrix()
        y_initial-=1
        translate(x_initial, y_initial, z_initial)
        drawHomer()
        popMatrix()
    elif (state == 2 and z_rot < PI/2 and y_rot > -PI/2):
        z_rot+=.01
        y_rot-=.01
    else:
        global state
        state+=1
    
    pushMatrix()
    translate(x_initial, y_initial, z_initial)
    rotateZ(z_rot)
    rotateY(y_rot)
    drawHomer()
    popMatrix()
    
def standing():
    pushMatrix()
    translate(x_initial, y_initial, z_initial)
    drawHomer()
    popMatrix()

def drawHomer():
    pushMatrix()
    scale(5, 5, 5)
    #transform the entire head
    pushMatrix()
    translate(0, -20, 0)
    scale(.5, .5, .5)
    drawHead()
    popMatrix()
    
    drawUpperBody()
    
    #left leg
    pushMatrix()
    translate(-3.25, 13, 0)
    drawLeg()
    popMatrix()
    
    #right leg
    pushMatrix()
    translate(3.25, 13, 0)
    drawLeg()
    popMatrix()
    
    #rotate entire character (close)
    popMatrix()

# cylinder with radius = 1, z range in [-1,1]
def cylinder(sides = 64):
    # first endcap
    beginShape()
    for i in range(sides):
        theta = i * 2 * PI / sides
        x = cos(theta)
        y = sin(theta)
        vertex ( x,  y, -1)
    endShape(CLOSE)
    # second endcap
    beginShape()
    for i in range(sides):
        theta = i * 2 * PI / sides
        x = cos(theta)
        y = sin(theta)
        vertex ( x,  y, 1)
    endShape(CLOSE)
    # sides
    x1 = 1
    y1 = 0
    for i in range(sides):
        theta = (i + 1) * 2 * PI / sides
        x2 = cos(theta)
        y2 = sin(theta)
        beginShape()
        normal (x1, y1, 0)
        vertex (x1, y1, 1)
        vertex (x1, y1, -1)
        normal (x2, y2, 0)
        vertex (x2, y2, -1)
        vertex (x2, y2, 1)
        endShape(CLOSE)
        x1 = x2
        y1 = y2
        

def drawHead():
    # top of head
    fill (255, 217, 15)
    pushMatrix()
    translate (0, -9, 0)
    sphereDetail(60)
    sphere(9.95)
    popMatrix()

    # face
    fill (255, 217, 15)
    pushMatrix()
    rotateX (PI/2)
    scale (10, 10, 10)
    cylinder()
    popMatrix()
    
    # left eye
    fill (255, 255, 255)
    pushMatrix()
    translate(-3.5, -4, 8)
    sphere(4)
    popMatrix()
    
    #left pupil
    fill (0, 0, 0)
    pushMatrix()
    translate(-5, -4, 11.5)
    sphere(0.5)
    popMatrix()
    
    # right eye
    fill (255, 255, 255)
    pushMatrix()
    translate(3.5, -4, 8)
    sphere(4)
    popMatrix()
    
    #right pupil
    fill (0, 0, 0)
    pushMatrix()
    translate(5, -4, 11.5)
    sphere(0.5)
    popMatrix()
    
    #nose
    fill (255, 217, 15)
    pushMatrix()
    translate(0, -1, 11)
    cylinder()
    popMatrix()
    
    pushMatrix()
    translate(0, -1, 12)
    sphere(1)
    popMatrix()
    
    #beard/mouth
    fill (209, 178, 112)
    pushMatrix()
    translate(0, 5, 7)
    sphere(5.5)
    popMatrix()
    
    noFill()
    stroke(20)
    pushMatrix()
    translate(0, 3.7, 11.5)
    rotateX(PI/4)
    arc(0, 0, 6, 3, 0, PI)
    popMatrix()

    #hair - front
    noFill()
    stroke(20)
    pushMatrix()
    translate(0, -17, -2)
    ellipse(0, 0, 10, 8)
    popMatrix()
    
    #hair - back
    noFill()
    stroke(20)
    pushMatrix()
    translate(0, -17, 2)
    ellipse(0, 0, 10, 8)
    popMatrix()
    
    #ears
    fill(255, 217, 15)
    noStroke()
    pushMatrix()
    translate(-10, 1, 0)
    scale(2, 2, .5)
    sphereDetail(60)
    sphere(1)
    popMatrix()
    
    fill(255, 217, 15)
    noStroke()
    pushMatrix()
    translate(10, 1, 0)
    scale(2, 2, .5)
    sphereDetail(60)
    sphere(1)
    popMatrix()
    

    
    
def drawUpperBody():
    noStroke()
    #shirt
    fill(255, 255, 255)
    pushMatrix()
    translate(0, -11, 0)
    sphere(5.5)
    popMatrix()
    pushMatrix()
    translate(0, -2, 0)
    sphereDetail(60)
    sphere(8)
    popMatrix()
    
    #part where pants meet shirt (blue)
    fill(79, 118, 223)
    pushMatrix()
    sphereDetail(60)
    sphere(8)
    popMatrix()
    
    #sleves
    #left
    fill(255, 255, 255)
    pushMatrix()
    translate(-7, -10, 0)
    scale(2, 2, 2)
    rotateY(PI/2)
    rotateX(PI/4)
    cylinder()
    popMatrix()
    pushMatrix()
    translate(-6, -11, 0)
    sphere(2)
    popMatrix()
    
    #right
    pushMatrix()
    translate(7, -10, 0)
    scale(2, 2, 2)
    rotateY(PI/2)
    rotateX(-PI/4)
    cylinder()
    popMatrix()
    pushMatrix()
    translate(6, -11, 0)
    sphere(2)
    popMatrix()
    
    #arms
    #left
    fill(255, 217, 15)
    pushMatrix()
    translate(-11, -4, 0)
    rotateX(PI/2)
    rotateY(PI/6)
    drawArm()
    popMatrix()
    
    #right
    fill(255, 217, 15)
    pushMatrix()
    translate(11, -4, 0)
    rotateX(PI/2)
    rotateY(-PI/6)
    drawArm()
    popMatrix()
    
    pushMatrix()
    translate(-14.5, 2.5, 0)
    drawHand()
    popMatrix()
    
    pushMatrix()
    translate(14.5, 2.5, 0)
    rotateY(PI)
    drawHand()
    popMatrix()
    
def drawArm():
    pushMatrix()
    scale(1.5, 1.5, 7)
    cylinder()
    popMatrix()
    
def drawLeg():
    #pants
    fill(79, 118, 223)
    pushMatrix()
    #translate(-3.25, 13, 0)
    #translate(0, 13, 0)
    rotateX(PI/2)
    scale(3, 3, 10)
    cylinder()
    popMatrix()
    
    #shoes
    fill(0, 0, 0)
    pushMatrix()
    translate(0, 10, 1.5)
    rotateX(PI/2)
    scale(2, 3, 1.5)
    sphereDetail(60)
    sphere(2)
    popMatrix()

def drawHand():
    #base
    pushMatrix()
    scale(1.5, 2, 1.5)
    rotateZ(PI/4)
    sphereDetail(60)
    sphere(1)
    popMatrix()
    
    #thumb
    pushMatrix()
    translate(-1.5, .25, 0)
    scale(.5, .5, .5)
    rotateY(PI/2)
    cylinder()
    popMatrix()
    #thumb tip
    pushMatrix()
    translate(-2, .25, 0)
    scale(.5, .5, .5)
    sphereDetail(60)
    sphere(1)
    popMatrix()
    
    #finger1
    pushMatrix()
    translate(-1.25, 1.5, 0)
    scale(.5, .5, .5)
    rotateY(PI/2)
    rotateX(PI/4)
    cylinder()
    popMatrix()
    #finger tip 1
    pushMatrix()
    translate(-1.75, 2, 0)
    scale(.5, .5, .5)
    sphereDetail(60)
    sphere(1)
    popMatrix()
    
    #finger2
    pushMatrix()
    translate(-.25, 2.25, 0)
    scale(.5, .5, .5)
    rotateY(PI/2)
    rotateX(PI/2)
    cylinder()
    popMatrix()
    #finger tip 2
    pushMatrix()
    translate(-.25, 2.75, 0)
    scale(.5, .5, .5)
    sphereDetail(60)
    sphere(1)
    popMatrix()
    
    #finger3
    pushMatrix()
    translate(1, 2, 0)
    scale(.5, .5, .5)
    rotateY(PI/2)
    rotateX(-PI/4)
    cylinder()
    popMatrix()
    #finger tip 3
    pushMatrix()
    translate(1.25, 2.25, 0)
    scale(.5, .5, .5)
    sphereDetail(60)
    sphere(1)
    popMatrix()