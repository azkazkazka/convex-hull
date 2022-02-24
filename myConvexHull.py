import numpy as np
import math

def inLine(p1, p2, p3):
    return ((math.dist(p1, p3) + math.dist(p2, p3)) == math.dist(p1, p2))

# returns -1 when point is in the left of a line and 1 when the opposite
def checkPosition(p1, p2, p3):
    p1 = np.append(p1, 1)
    p2 = np.append(p2, 1)
    p3 = np.append(p3, 1)
    temp = [p1, p2, p3]
    det = np.linalg.det(temp)
    if det < 0:
        return 1
    else:
        return -1

def getAngle(p1, p2, p3):
    p1x, p1y = p1[0] - p3[0], p1[1] - p3[1]
    p2x, p2y = p2[0] - p3[0], p2[1] - p3[1]
    a = math.atan2(p1x, p1y)
    b = math.atan2(p2x, p2y)
    if a < 0:
        a += math.pi * 2
    if b < 0:
        b += math.pi * 2
    if (a > b):
        return (math.pi * 2 + b - a)
    else:
        return b - a

def getFarthest(p1, p2, list):
    farthest = [0, 0] # distance + angle
    for arr in list:
        angle = getAngle(p1, p2, arr)
        dist = math.dist(p1, arr) + math.dist(p2, arr)
        if (dist > farthest[0] or (dist == farthest and angle > farthest[1])):
            farthest[0] = dist
            farthest[1] = angle
            point = arr
    return point # return distance only

def getExtremes(arr):
    arr = arr[arr[:, 0].argsort()]
    minPoint = arr[0]
    maxPoint = arr[-1]
    return minPoint, maxPoint

def insideTriangle(area, p1, p2, pmax):
    for arr in area:
        if not(inLine(p1, p2, arr) or inLine(p1, pmax, arr) or inLine(pmax, p2, arr)):
            if (arr[0] <= pmax[0] and checkPosition(p1, pmax, arr) == 1):
                np.delete(area, np.argwhere(area == arr))
            elif (arr[0] >= pmax[0] and checkPosition(pmax, p2, arr) == -1):
                np.delete(area, np.argwhere(area == arr))
        else:
            np.delete(area, np.argwhere(area == arr))

def divideArea(arr2D, p1, p2, int):
    upper = []
    lower = []
    np.delete(arr2D, np.argwhere(arr2D == p1))
    np.delete(arr2D, np.argwhere(arr2D == p2))

    # get left and right side
    for arr in arr2D:
        if not(inLine(p1, p2, arr)):
            if (checkPosition(p1, p2, arr) == -1):
                upper.append(arr)
            else:
                lower.append(arr)
        else:
            np.delete(arr2D, np.argwhere(arr2D == arr))
    
    # check upper area
    if (int >= 0):
        if (not (upper)):
            result.append([p1, p2])
        else:
            farthest = getFarthest(p1, p2, upper)
            insideTriangle(upper, p1, p2, farthest)
            divideArea(upper, p1, farthest, 1)
            divideArea(upper, farthest, p2, 1)

    # check lower area
    if (int <= 0):        
        if (not (lower) and int <= 0):
            result.append([p1, p2])
        else:
            farthest = getFarthest(p1, p2, lower)
            insideTriangle(lower, p1, p2, farthest)
            divideArea(lower, p1, farthest, -1)
            divideArea(lower, farthest, p2, -1)
        return

def convexHull(bucket):
    global result
    result = []
    arr2D = np.copy(bucket)
    minPoint, maxPoint = getExtremes(arr2D)
    arr2D = arr2D[arr2D[:, 0].argsort()]
    for i in arr2D:
        print(i[0], i[1])
    # mulai loop dari sini
    divideArea(arr2D, minPoint, maxPoint, 0)
    print(result)
    return result



import matplotlib.pyplot as plt
from sklearn import datasets
import pandas as pd
import numpy as np
# from convexhull import convexHull

# iris = datasets.load_iris()
# print('The data matrix:\n',iris['data'])
# print('The classification target:\n',iris['target'])
# print('The names of the dataset columns:\n',iris['feature_names'])
# print('The names of target classes:\n',iris['target_names'])
# print('The full description of the dataset:\n',iris['DESCR'])
# print('The path to the location of the data:\n',iris['filename'])

data = datasets.load_iris()
#create a DataFrame
df = pd.DataFrame(data.data, columns=data.feature_names)
print(data.target)
df['Target'] = pd.DataFrame(data.target)
print(df.shape)
df.head()

plt.figure(figsize = (10, 6))
colors = ['b','r','g']
plt.title('Petal Width vs Petal Length')
plt.xlabel(data.feature_names[0])
plt.ylabel(data.feature_names[1])
for i in range(len(data.target_names)):
    bucket = df[df['Target'] == i]
    bucket = bucket.iloc[:,[0,1]].values
    hull = convexHull(bucket) #bagian ini diganti dengan hasil implementasi
    plt.scatter(bucket[:, 0], bucket[:, 1], label=data.target_names[i])
    for simplex in hull:
        print(simplex[0], simplex[1])
        plt.plot([simplex[0][0], simplex[1][0]], [simplex[0][1], simplex[1][1]], colors[i])
plt.legend()
plt.show()