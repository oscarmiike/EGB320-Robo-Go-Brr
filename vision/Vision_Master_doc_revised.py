    
import numpy as np
import cv2
import math
import random as rng
import picamera2
import time
import threading


def find_lowest_point(mask,size_x,size_y,act): #This takes the input colour mask and size restraints
    if act==0:
        mask = cv2.erode(mask,(cv2.getStructuringElement(cv2.MORPH_RECT, (7,7),(2,2) )))
        mask = cv2.dilate(mask,(cv2.getStructuringElement(cv2.MORPH_RECT, (12,10),(2,2) )))
        cv2.rectangle(mask, (0, 0), (320, 240), (0,0,0), 2)
    else:
        mask = cv2.erode(mask,(cv2.getStructuringElement(cv2.MORPH_RECT, (7,7),(2,2) )))
        mask = cv2.dilate(mask,(cv2.getStructuringElement(cv2.MORPH_RECT, (15,15),(2,2) )))
        cv2.rectangle(mask, (0, 0), (320, 240), (0,0,0), 2)    
        # cv2.imshow("Changed", mask)
    edges =cv2.Canny(mask,50,50) #It finds all the edges of the masks
    #cv2.imwrite(filepath+"edges.png",edges)
    contours,__ =cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #Finds the contours
    #Initialising variables to store data
    points_to_check=[]
    valid_rect=[]
    i=0
    biggest=[]
    final_array=[]
    maxi=0

    #Now we index through the contours
    for i, c in enumerate(contours):

        contours_poly = cv2.approxPolyDP(c, 3, True) #approximates a polygon of +/-3
        rect=cv2.boundingRect(contours_poly)  # Creates a bounding rectangle

        if rect[2]>size_x and rect[3]>size_y: #Checks to see if the rectangle is greater then the constraints

            if (i%2)==0:
 
                points_to_check.append([math.ceil(rect[0]+rect[2]/2),(rect[1]+rect[3])]) 
                #Adds the middle value
                valid_rect.append(rect)
                #appends the topleft corner+ width and height
                
                
    # for item in valid_rect:
    #     if item[2]*item[3]>maxi:
    #         maxi=item[2]*item[3]
    #         biggest=item
    #         j=i
    #     i=i+1
        
    # if len(biggest)>0:
    #     final_array.append(biggest)
    # i=0 
    # for item in valid_rect:
    #     if j!=i:
    #         final_array.append(item)
        
    return(points_to_check,valid_rect) 



def Pinhole_dist(Height,obstacle_height,bearing):
    return(abs(obstacle_height/Height*267/math.cos(bearing/180*math.pi))) ##originally 267  changed to 137

def Pinhole_Width(Width,obstacle_width,bearing):
    return(abs(obstacle_width/Width*267/math.cos(bearing)))

def find_Bearing(x_pos):
    #print(x_pos)
    relative_pos=x_pos-160
    Angle=relative_pos/160*36.5
    return(Angle)


def Find_Aisle(mask,radius_min,radius_max): #This takes the input colour mask and size restraints
    mask = cv2.erode(mask,(cv2.getStructuringElement(cv2.MORPH_RECT, (4,4),(2,2) )))
    mask = cv2.dilate(mask,(cv2.getStructuringElement(cv2.MORPH_RECT, (5,5),(2,2) )))
    cv2.rectangle(mask, (0, 0), (320, 240), (0,0,0), 2)
    edges =cv2.Canny(mask,50,50) #It finds all the edges of the masks
    cv2.imshow("Mask", mask)
    cv2.imshow("Edges",edges)
    contours,_ =cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #Finds the contours

    #Initialising variables to store data
    rectangles=[]

    #Now we index through the contours
    for i, c in enumerate(contours):
        contours_poly = cv2.approxPolyDP(c, 3, True) #approximates a polygon of +/-3
        rect=cv2.boundingRect(contours_poly)  # Creates a bounding rectangle
        if radius_min<rect[2]<radius_max:
            rectangles.append(rect)
            
    return(rectangles) 


def Colour_checker(image, point):
    sub_value=10
    i=0
    Lower_Floor = np.array([0,0,80,0])
    Upper_Floor = np.array([255,25,170,256])
    checked=False
    valid=0
    ##Starting with left
    #print("The Length is....."+str(len(image[1])))
    while i<3:
        new_value=point[1]+(sub_value*i)
        if new_value>=240:
            new_value=239
            #print("activated")
        if (Upper_Floor>image[new_value,point[0]]).all and (image[new_value,point[0]]>Lower_Floor).all:
            if checked==False:
                valid=[point[0],point[1]]
                checked=True
                ##Up to date 2222
        i=i+1

    if valid==False:
        return(0,0)
    else:
        return (valid)


def Colour_Seperator(frame):
    #frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)  ## COnversion into HSV for the Hue channel

    #Masks
    #redmask = cv2.inRange(frame, lower_red, upper_red)
    whitemask =cv2.inRange(frame,lower_white, upper_white)
    bluemask = cv2.inRange(frame, lower_blue, upper_blue)
    greenmask = cv2.inRange(frame, Lower_green, Upper_green)
    yellowmask = cv2.inRange(frame, lower_yellow, upper_yellow)
    mark_mask =cv2.inRange(frame, Lower_Mark, Upper_Mark)
    return(bluemask,greenmask,yellowmask, mark_mask,whitemask)




def Vision_init():
    #Colour Cutoffs
    global lower_blue 
    global upper_blue
    global lower_yellow 
    global upper_yellow
    global Lower_green 
    global Upper_green
    global Lower_Mark
    global Upper_Mark
    global lower_red
    global upper_red
    global lower_white
    global upper_white

    lower_blue = np.array([90,70,40])
    upper_blue = np.array([115,256,256])

    lower_white = np.array([25,40,195])
    upper_white = np.array([40, 130,232])

    lower_yellow = np.array([20,180,200])
    upper_yellow = np.array([30,256,256])

    Lower_green = np.array([47,70,40])
    Upper_green = np.array([90,255,255])

 

    # Lower_Mark =np.array([24,0,0])  # Day Time
    # Upper_Mark =np.array([53,256,77]) 

    Lower_Mark =np.array([24,0,0])
    Upper_Mark =np.array([53,256,90])  #NIGHT TIME


    lower_red = np.array([5,70,100])
    upper_red = np.array([20,256,256])
    global cap
    global config
    cap = picamera2.Picamera2()
    config = cap.create_video_configuration(main={"format":'XRGB8888',"size":(820,616)})
    cap.configure(config)
    cap.set_controls({"ColourGains": (1.4,1.5)})
    cap.start()


def Red_bearing(hsv_frame,frame):
    red =cv2.inRange(hsv_frame, lower_red, upper_red)
    check, rectangles =find_lowest_point(red,5,5,0)
    Red_bearings=[]
    height=0
    max=100
    if len(rectangles)>0:
        i=0
        for rect in rectangles:
            bear=find_Bearing(check[i][0])
            Red_bearings.append(bear)
            cv2.rectangle(frame, (int(rect[0]), int(rect[1])), (int(rect[0]+rect[2]), int(rect[1]+rect[3])), (0,0,256), 2)
            cv2.putText(frame, ("Item:"+str(i)),[check[i][0]-10,check[i][1]-5], cv2.FONT_HERSHEY_SIMPLEX, 0.3, [255,255,255], 1, cv2.LINE_AA)
            cv2.putText(frame, (str(int(bear))+"Deg"), [check[i][0]-10,check[i][1]-20], cv2.FONT_HERSHEY_SIMPLEX, 0.3, [255,255,255], 1, cv2.LINE_AA)
            i=i+1
        i=0
        for element in Red_bearings:
            if abs(element)<abs(max):
                max=element
                height=rectangles[i][3]
                i=i+1
    return max,frame,height,rectangles




                







def Main_Outline(frame, hsv_frame):
    In_Aisle=True
    blue,green,yellow, mark,white = Colour_Seperator(hsv_frame)

    
    # FINDING THE OBSTACLES
    check, rectangles =find_lowest_point(green,9,25,0)
    green_dist=[]
    green_bearing=[]
    if len(rectangles) >0:
        i=0
        for rect in rectangles:
            bear=find_Bearing(check[i][0])
            dist=Pinhole_dist(rect[3],150,bear)
            green_bearing.append(bear)
            green_dist.append(dist)
            #print("Distance to obstacle at..."+str(dist))
            
            #print("bearing to obstacle at..."+str(bear))
            #print(rect[3]) 
            cv2.rectangle(frame, (int(rect[0]), int(rect[1])), (int(rect[0]+rect[2]), int(rect[1]+rect[3])), (0,256,0), 2)
            cv2.putText(frame, ("OB:"+str(i)),[check[i][0]-10,check[i][1]-5], cv2.FONT_HERSHEY_SIMPLEX, 0.3, [255,255,255], 1, cv2.LINE_AA)
            cv2.putText(frame, (str(int(bear))+"deg"), [check[i][0]-10,check[i][1]-20], cv2.FONT_HERSHEY_SIMPLEX, 0.3, [255,255,255], 1, cv2.LINE_AA)
            cv2.putText(frame, (str(int(dist))+"mm"),[check[i][0]-10,check[i][1]-35], cv2.FONT_HERSHEY_SIMPLEX, 0.3, [255,255,255], 1, cv2.LINE_AA)
            i=i+1

    
    ################### Finding the Return Bay
    #print("starting Yellow")
    check, rectangles =find_lowest_point(yellow,10,10,0)
    yel_dist=[]
    yel_dist2=[]
    yel_bearing=[]
    yrects=rectangles
    if len(rectangles) >0:
        In_Aisle=False
        i=0
        for rect in rectangles:
            bear=find_Bearing(check[i][0])
            dist=Pinhole_dist(rect[3],60,bear)
            dist2=Pinhole_Width(rect[2],120,bear)
            yel_bearing.append(bear)
            yel_dist.append(dist)
            yel_dist2.append(dist2)
            cv2.rectangle(frame, (int(rect[0]), int(rect[1])), (int(rect[0]+rect[2]), int(rect[1]+rect[3])), (0,256,256), 2)
            cv2.putText(frame, ("RB:"+str(i)),[check[i][0]-10,check[i][1]-5], cv2.FONT_HERSHEY_SIMPLEX, 0.3, [255,255,255], 1, cv2.LINE_AA)
            cv2.putText(frame, (str(int(bear))+"deg"), [check[i][0]-10,check[i][1]-20], cv2.FONT_HERSHEY_SIMPLEX, 0.3, [255,255,255], 1, cv2.LINE_AA)
            cv2.putText(frame, (str(int(dist))+"mm"),[check[i][0]-10,check[i][1]-35], cv2.FONT_HERSHEY_SIMPLEX, 0.3, [255,255,255], 1, cv2.LINE_AA)
            i=i+1


    # #Finding the Collection Aisles
    #print("starting Blue")
    blue_bearing=[]
    blue_dist=[]
    check, rectangles =find_lowest_point(blue,15,25,0)
    if len(rectangles) >0:
        i=0
        for rect in rectangles:
            bear=find_Bearing(check[i][0])
            dist=Pinhole_dist(rect[3],310,bear)
            blue_bearing.append(bear)
            blue_dist.append(dist)
            cv2.rectangle(frame, (int(rect[0]), int(rect[1])), (int(rect[0]+rect[2]), int(rect[1]+rect[3])), (256,0,0), 2)    
            cv2.putText(frame, ("shelf:"+str(i)),[check[i][0]-10,check[i][1]-5], cv2.FONT_HERSHEY_SIMPLEX, 0.3, [255,255,255], 1, cv2.LINE_AA)
            cv2.putText(frame, (str(int(bear))+"deg"), [check[i][0]-10,check[i][1]-20], cv2.FONT_HERSHEY_SIMPLEX, 0.3, [255,255,255], 1, cv2.LINE_AA)
            cv2.putText(frame, (str(int(dist))+"mm"),[check[i][0]-10,check[i][1]-35], cv2.FONT_HERSHEY_SIMPLEX, 0.3, [255,255,255], 1, cv2.LINE_AA)
            i=i+1




    ##################### AISLE MARKERS ###########################
    mark = mark[0:-1,:]  #Crops the image
    black_bearing=[]
    black_dist=[]
    prev_bear=0
    bear_max=0
    condition=0
    max_height=1000
    bearing=0
    if In_Aisle==True:
        #print("in Aisle")
        rectangles=Find_Aisle(mark, 9, 150) #4 during day
        i=0
        if len(rectangles)>0:
            for rect in rectangles:
                point=round((rect[2])/2)
                point=point+rect[0]
                y=rect[1]
                cv2.rectangle(frame, (int(rect[0]), int(rect[1])), (int(rect[0]+rect[2]), int(rect[1]+rect[3])), (128,0,128), 2)
                bear=find_Bearing(rect[0]+rect[2]/2)
                if abs(bear +prev_bear)>25:
                    condition=1
                bear_max=bear_max+bear
                prev_bear=bear
                dist=int(Pinhole_dist(rect[3],70,bear))
                cv2.putText(frame, (str(int(bear))+"deg"), [point,y+25], cv2.FONT_HERSHEY_SIMPLEX, 0.3, [128,0,128], 1, cv2.LINE_AA)
                cv2.putText(frame, (str(int(dist))+"mm"),[point,y+35], cv2.FONT_HERSHEY_SIMPLEX, 0.3, [128,0,128], 1, cv2.LINE_AA)
                black_bearing.append(bear)
                black_dist.append(dist)   
                #print("The Values are Pixel Height: "+str(rect[3])+" Bearing: "+str(bear)+" And distance: "+ str(dist))
                i=i+1
            if len(rectangles)<7 and (condition==0):
                black_bearing.insert(0,(bear_max/len(black_dist)))
                print("average used")
            else:
                for rect in rectangles:
                    if rect[1]<max_height:
                        max_height=rect[1]
                        bearing=find_Bearing(rect[0]+rect[2]/2)
                black_bearing.insert(0,bearing)
                        
            print("The current target is... "+str(black_bearing[0]))
        aisle_number=len(rectangles)/2
        #print("You Are In aisle_number:" +str(aisle_number))
       
    else:
        aisle_number=0
        rectangles=Find_Aisle(mark, 2, 150)
        edges =cv2.Canny(mark,50,50) #It finds all the edges of the masks
        cv2.imshow("Edges",edges)
        i=0
        if len(rectangles)>0:
            for rect in rectangles:
                point=round((rect[2])/2)
                point=point+rect[0]
                y=rect[1]
                cv2.rectangle(frame, (int(rect[0]), int(rect[1])), (int(rect[0]+rect[2]), int(rect[1]+rect[3])), (128,0,128), 2) 
                bear=find_Bearing(rect[0]+rect[2]/2)
                bear_max=bear_max+bear
                dist=Pinhole_dist(rect[3],70,bear)
                print("The Values are Pixel Height: "+str(rect[3])+" Bearing: "+str(bear)+" And distance: "+ str(dist))
                cv2.putText(frame, (str(int(bear))+"deg"), [point,y+25], cv2.FONT_HERSHEY_SIMPLEX, 0.3, [128,0,128], 1, cv2.LINE_AA)
                cv2.putText(frame, (str(int(dist))+"mm"),[point,y+35], cv2.FONT_HERSHEY_SIMPLEX, 0.3, [128,0,128], 1, cv2.LINE_AA)
                black_bearing.append(bear)
                black_dist.append(dist)   
                i=i+1  
                i=i+1
            black_bearing.insert(0,(bear_max/len(black_dist)))

    ######### I'M IN YOUR WALLS ##########################
    wall_dists=[]
    wall_bearings=[]

    check, rectangles =find_lowest_point(white,40,50,1)
    
    #cv2.imshow("Whitemask",white)  ##Shows the trial frame
    if len(rectangles) >0:
        i=0
        for rect in rectangles:
            bear=find_Bearing(check[i][0])
            dist=(rect[3]/1417)**-2.571
            wall_dists.append(dist)
            wall_bearings.append(bear)
            #print("The Size is....." +str(rect[3]))
            #time.sleep(0.1)
            cv2.rectangle(frame, (int(rect[0]), int(rect[1])), (int(rect[0]+rect[2]), int(rect[1]+rect[3])), (0,0,0), 2)    
            cv2.putText(frame, ("WALL:"+str(i)),[check[i][0]-10,check[i][1]-5], cv2.FONT_HERSHEY_SIMPLEX, 0.3, [0,0,0], 1, cv2.LINE_AA)
            cv2.putText(frame, (str(int(bear))+"deg"), [check[i][0]-10,check[i][1]-20], cv2.FONT_HERSHEY_SIMPLEX, 0.3, [255,255,255], 1, cv2.LINE_AA)
            cv2.putText(frame, (str(int(dist))+"mm"),[check[i][0]-10,check[i][1]-35], cv2.FONT_HERSHEY_SIMPLEX, 0.3, [0,0,0], 1, cv2.LINE_AA)
            i=i+1


                

    return(green_bearing,green_dist,yel_bearing,yel_dist,yel_dist2,yrects,blue_bearing,blue_dist,black_bearing,black_dist,aisle_number,wall_bearings,wall_dists)

