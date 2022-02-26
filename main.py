import numpy as np 
import pandas as pd 
from sklearn import datasets 
import matplotlib.pyplot as plt 
from myConvexHull import convexHull

def pickData():
    """Get user chosen data and columns out of 3 available datasets"""
    
    # print list of available datasets
    print("List of available datasets")
    print("1. Iris")
    print("2. Wine")
    print("3. Breast Cancer")

    # initialize dataset choice
    choice = int(input("Enter dataset number: "))
    if (choice == 1):
        data = datasets.load_iris()
        datasetname = "Iris"
    elif (choice == 2):
        data = datasets.load_wine()
        datasetname = "Wine"
    else:
        data = datasets.load_breast_cancer()
        datasetname = "Breast Cancer"
    df = pd.DataFrame(data.data, columns=data.feature_names)

    # initialize column choices
    print("--------------------------------------------------------")
    print("List of available columns in " + datasetname + " dataset")
    i = 1
    for col in df.columns:
        print(str(i) + ". " + str(col))
        i += 1
    print("Enter two column numbers to test linear separability")
    x = int(input("First column number: ")) - 1
    y = int(input("Second column number: ")) - 1
    title = (df.columns[x] + " vs " + df.columns[y])

    # process data through acquired choices
    processData(data, df, x, y, title)

def processData(data, df, x, y, title):
    """Mendapatkan hasil visualisasi tes linear separability dataset"""

    # mengambil target klasifikasi
    df['Target'] = pd.DataFrame(data.target)

    # visualisasi data
    plt.figure(figsize = (10, 6))
    colors = ['b','r','g']
    plt.title(title)
    plt.xlabel(data.feature_names[x])
    plt.ylabel(data.feature_names[y])
    # mencari convex hull untuk setiap target
    for i in range(len(data.target_names)):
        bucket = df[df['Target'] == i]
        bucket = bucket.iloc[:,[x,y]].values
        hull = convexHull(bucket)
        plt.scatter(bucket[:, 0], bucket[:, 1], label=data.target_names[i])
        for simplex in hull:
            plt.plot([simplex[0][0], simplex[1][0]], [simplex[0][1], simplex[1][1]], colors[i % 3])
    plt.legend()
    plt.show()

pickData()