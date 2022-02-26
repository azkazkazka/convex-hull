import numpy as np
import math

def getExtremes(arr):
    """Returns leftmost and rightmost point"""
    
    arr = arr[arr[:, 0].argsort()] # sort based on x - coordinate
    minPoint = arr[0]
    maxPoint = arr[-1]
    return minPoint, maxPoint

def inLine(p1, p2, p3):
    """Returns true if p3 is in line (check by distance)"""

    return ((math.dist(p1, p3) + math.dist(p2, p3)) == math.dist(p1, p2))

def checkPosition(p1, p2, p3):
    """Checks position of p3 relative to p1 and p2 through determinant
    
    Return 1 when p3 is in rightside and -1 when p3 is in leftside"""

    # init matrix
    p1 = np.append(p1, 1)
    p2 = np.append(p2, 1)
    p3 = np.append(p3, 1)
    temp = [p1, p2, p3]

    det = np.linalg.det(temp) 
    if det < 0:
        return 1 # p3 in rightside
    else:
        return -1 # p3 in leftside

def getAngle(p1, p2, p3):
    """Return angle between p1, p3, and p2"""

    p1x, p1y = p1[0] - p3[0], p1[1] - p3[1]
    a1 = math.atan2(p1x, p1y) # find arctan
    if a1 < 0: # negative case
        a1 += math.pi * 2 
    p2x, p2y = p2[0] - p3[0], p2[1] - p3[1]
    a2 = math.atan2(p2x, p2y) # find arctan
    if a2 < 0: # negative case
        a2 += math.pi * 2 
    if (a1 > a2): # negative case
        return (math.pi * 2 + a2 - a1)
    else:
        return a2 - a1

def getFarthest(p1, p2, list):
    """Return farthest point from p1 and p2"""

    farthest = [0, 0] # store distance and angle for comparison
    for arr in list: 
        angle = getAngle(p1, p2, arr) # get angle for pmax comparison
        dist = math.dist(p1, arr) + math.dist(p2, arr) # get distance p1-point-p2
        if (dist > farthest[0] or (dist == farthest and angle > farthest[1])):
            farthest[0] = dist
            farthest[1] = angle
            point = arr
    return point # return farthest point only

def insideTriangle(area, p1, p2, pmax):
    """Remove points inside triangle with points p1, p2, and pmax"""

    for arr in area:
        # check if point in triangle line
        if not(inLine(p1, p2, arr) or inLine(p1, pmax, arr) or inLine(pmax, p2, arr)):
            # check if point in leftside of pmax and rightside of line pmax-p2
            if (arr[0] <= pmax[0] and checkPosition(p1, pmax, arr) == 1):
                np.delete(area, np.argwhere(area == arr))
            # check if point in rightside of pmax and leftside of line pmax-p2
            elif (arr[0] >= pmax[0] and checkPosition(pmax, p2, arr) == -1):
                np.delete(area, np.argwhere(area == arr))
        else:
            np.delete(area, np.argwhere(area == arr))

def divideArea(arr2D, p1, p2, int):
    """Find sets by dividing areas based on line with points p1 and p2
    
    Arr2D is filled with all points to be checked and int indicates recursion phase 
    (0 for first recursion, 1 for upper area recursion, -1 for lower area recursion"""

    np.delete(arr2D, np.argwhere(arr2D == p1))
    np.delete(arr2D, np.argwhere(arr2D == p2))
    # list for storing points to be checked
    upper = []
    lower = []

    for arr in arr2D:
        if not(inLine(p1, p2, arr)):
            # if point above line, add point to upper list
            if (checkPosition(p1, p2, arr) == -1):
                upper.append(arr)
            # if point below line, add point to lower list
            else:
                lower.append(arr) 
        else:
            np.delete(arr2D, np.argwhere(arr2D == arr))
    
    # continue checking upper area for init and upper area recursion
    if (int >= 0):
        if (not(upper)):
            result.append([p1, p2]) # add line to end result if upper list is empty
        else:
            farthest = getFarthest(p1, p2, upper) # get pmax
            insideTriangle(upper, p1, p2, farthest) # remove inside triangle
            divideArea(upper, p1, farthest, 1) # leftside upper area recursion
            divideArea(upper, farthest, p2, 1) # rightside upper area recursion

    # continue checking lower area for init and lower area recursion
    if (int <= 0):
        if (not(lower)): 
            result.append([p1, p2]) # add line to end result if lower list is empty
        else:
            farthest = getFarthest(p1, p2, lower) # get pmax
            insideTriangle(lower, p1, p2, farthest) # remove inside triangle
            divideArea(lower, p1, farthest, -1) # leftside lower area recursion
            divideArea(lower, farthest, p2, -1) # rightside lower area recursion

def convexHull(bucket):
    """Returns list of lines that make up convex hull
    by implementing divide and conquer algorithm"""

    # initialize variables
    global result
    result = []
    arr2D = np.copy(bucket)
    # get two starting points
    minPoint, maxPoint = getExtremes(arr2D)
    # find lines for convex hull
    divideArea(arr2D, minPoint, maxPoint, 0) # first recursion
    return result