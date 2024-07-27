    
import numpy as np
import cv2
import math
import random as rng
import time
import concurrent.futures as cf

"""
▀█ █▀ ▀█▀ █▀▀ ▀█▀ █▀▀█ █▀▀▄ 
 █▄█   █  ▀▀█  █  █  █ █  █ 
  ▀   ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀▀ ▀  ▀ 
  
added: 10/09/2024
"""

def find_lowest_point(mask,size_x,size_y): #This takes the input colour mask and size restraints
    mask = cv2.erode(mask,(cv2.getStructuringElement(cv2.MORPH_RECT, (5,5),(2,2) )))
    mask = cv2.dilate(mask,(cv2.getStructuringElement(cv2.MORPH_RECT, (14,14),(2,2) )))
    mask = cv2.dilate(mask,(cv2.getStructuringElement(cv2.MORPH_RECT, (14,14),(2,2) )))
    edges =cv2.Canny(mask,50,50) #It finds all the edges of the masks
    contours,_ =cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #Finds the contours

    #Initialising variables to store data
    points_to_check=[]
    valid_rect=[]

    #Now we index through the contours
    for i, c in enumerate(contours):
        contours_poly = cv2.approxPolyDP(c, 3, True) #approximates a polygon of +/-3
        rect=cv2.boundingRect(contours_poly)  # Creates a bounding rectangle
        if rect[2]>size_x and rect[3]>size_y: #Checks to see if the rectangle is greater then the constraints
            points_to_check.append([math.ceil((rect[0]+rect[2])/2),(rect[1]-rect[3])]) 
            #Adds the middle value
            valid_rect.append(rect)
            #appends the topleft corner+ width and height
    
    return(points_to_check,valid_rect) 


def Find_Aisle(mask,radius_min): #This takes the input colour mask and size restraints
    mask = cv2.erode(mask,(cv2.getStructuringElement(cv2.MORPH_RECT, (5,5),(2,2) )))
    mask = cv2.dilate(mask,(cv2.getStructuringElement(cv2.MORPH_RECT, (14,14),(2,2) )))
    mask = cv2.dilate(mask,(cv2.getStructuringElement(cv2.MORPH_RECT, (14,14),(2,2) )))
    edges =cv2.Canny(mask,50,50) #It finds all the edges of the masks
    contours,_ =cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #Finds the contours

    #Initialising variables to store data
    centers=[]
    radii=[]

    #Now we index through the contours
    for i, c in enumerate(contours):
        contours_poly = cv2.approxPolyDP(c, 3, True) #approximates a polygon of +/-3
        center, rad = cv2.minEnclosingCircle(contours_poly[i])
        if rad>radius_min:
            centers.append(center )
            radii.append(rad)
            
    return(centers,radii) 

def check_applicability(contour, point):
    valid=[]
    invalid=False
    check=cv2.pointPolygonTest(contour,(point[0],point[1]),True)
    if check==1:
        valid.append(point[0],point[1])
    else:
        check=cv2.pointPolygonTest(contour,(point[0],point[1]-30),True)
        if check==1:
            valid.append(point[0],point[1])
        else:
            invalid=True

    check=cv2.pointPolygonTest(contour,(point[2],point[3]),True)
    if check==1:
        valid.append(point[2],point[3])
    else:
        check=cv2.pointPolygonTest(contour,(point[2],point[3]),True)
        if check==1:
            valid.append(point[2],point[3])
        else:
            invalid=True
    return(invalid,valid)
    

def Colour_checker(image, point):
    sub_value=10
    i=0
    Lower_Floor = np.array([0,0,80])
    Upper_Floor = np.array([255,25,170])
    checked=False
    valid=0

    ##Starting with left
    while i<3:
        if (Upper_Floor>image[point[0]-(sub_value*i),point[1]]).all and (image[point[0]-(sub_value*i),point[1]]>Lower_Floor).all:
            if checked==False:
                valid=[point[0],point[1]]
                checked=True
        i=i+1
    if valid==False:
        return(0,0)
    else:
        return (valid)


def CreateContour(mask):
    mask = cv2.erode(mask,(cv2.getStructuringElement(cv2.MORPH_RECT, (5,5),(2,2) )))
    mask = cv2.dilate(mask,(cv2.getStructuringElement(cv2.MORPH_RECT, (14,14),(2,2) )))
    mask = cv2.dilate(mask,(cv2.getStructuringElement(cv2.MORPH_RECT, (14,14),(2,2) )))
    mask = cv2.dilate(mask,(cv2.getStructuringElement(cv2.MORPH_RECT, (14,14),(2,2) )))
    max=0 #Initialise maximum size
    edges =cv2.Canny(mask,50,50) #It finds all the edges of the masks
    contours,_ =cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #Finds the contours
    for i, c in enumerate(contours): #Goes through the list of contours
        Contour_Area=cv2.arcLength(c,True)  #finds the maximum area
        if Contour_Area>max:  # If the contour area is greater then the max
            max=Contour_Area  #it sets a new max
            largest_contour=c   #and appends the contour as the largest
    return(largest_contour)


def Colour_Seperator(frame):
    #frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)  ## COnversion into HSV for the Hue channel


    #Colour Cutoffs
    #lower_red = np.array([5,70,70])
    #upper_red = np.array([20,256,256])

    lower_blue = np.array([90,70,70])
    upper_blue = np.array([115,256,256])

    lower_yellow = np.array([22,70,70])
    upper_yellow = np.array([25,256,256])

    Lower_green = np.array([60,70,70])
    Upper_green = np.array([90,255,255])

    Lower_Mark =np.array([95,30,25])
    Upper_Mark =np.array([102,154,41])

    #Masks
    #redmask = cv2.inRange(frame, lower_red, upper_red)
    begin_colour=time.perf_counter()

    # with cf.ProcessPoolExecutor() as executor:
    #     f1 =executor.submit(cv2.inRange,frame,lower_blue,upper_blue)
    #     f2 =executor.submit(cv2.inRange,frame,Lower_green, Upper_green)
    #     f3 =executor.submit(cv2.inRange,frame,lower_yellow, upper_yellow)
    #     f4 =executor.submit(cv2.inRange,frame,Lower_Mark, Upper_Mark)
    #     bluemask =f1.result()
    #     greenmask=f2.result()
    #     yellowmask=f3.result()
    #     mark_mask=f4.result()
    


    bluemask = cv2.inRange(frame,lower_blue,lower_blue)
    greenmask = cv2.inRange(frame, Lower_green, Upper_green)
    yellowmask = cv2.inRange(frame, lower_yellow, upper_yellow)
    mark_mask =cv2.inRange(frame, Lower_Mark, Upper_Mark)
    end_colour=time.perf_counter()
    print("It took....."+str(end_colour-begin_colour))
    return(bluemask,greenmask,yellowmask, mark_mask)

def Wall_distance(frame):
    Lower_Wall = np.array([0,0,204])
    Upper_Wall = np.array([30,10,255])
    Wallmask   =cv2.inRange(frame, Lower_Wall, Upper_Wall)
    

def Main_Outline(photo,hsv_photo):
    blue,green,yellow, mark= Colour_Seperator(hsv_frame)
  
    
    # FINDING THE OBSTACLES
    check, rectangles =find_lowest_point(green,100,300)
    if len(rectangles) >0:
        i=0
        for rect in rectangles:
            cv2.rectangle(photo, (int(rect[0]), int(rect[1])), (int(rect[0]+rect[2]), int(rect[1]+rect[3])), (0,256,0), 2)
            displacement=Colour_checker(photo,check[0])      
            cv2.putText(frame, ("Obstacle:"+str(i)),[displacement[1],displacement[0]], cv2.FONT_HERSHEY_SIMPLEX, 5, [255,255,255], 2, cv2.LINE_AA)
            i+=1
    

    
    # Finding the return bay

    check, rect =find_lowest_point(yellow,100,300)
    i=0
    if len(rect) >0:
        cv2.rectangle(photo, (int(rect[i][0]), int(rect[i][1])),
            (int(rect[i][0]+rect[i][2]), int(rect[i][1]+rect[i][3])), (256,256,0), 2)


    #Finding the Collection Aisles

    check, rect =find_lowest_point(blue,200,300)
    i=0
    if len(rect) >0:
        cv2.rectangle(photo, (int(rect[i][0]), int(rect[i][1])),
            (int(rect[i][0]+rect[i][2]), int(rect[i][1]+rect[i][3])), (256,0,0), 2)
        
    return photo




####################### MAIN ###################################
if __name__ == '__main__':
    start=time.time()
    frames =['Photo.jpeg','Photo2.jpg','Photo3.jpg','Photo3.png']
    frame=cv2.imread(frames[2])
    hsv_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)  ## COnversion into HSV for the Hue channel
    frame=Main_Outline(frame, hsv_frame)
    end=time.time()
    print(end-start)
    #cv2.imshow("Outlines",frame)
    #cv2.waitKey(20000)
    