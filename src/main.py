import pandas as pd 
from sklearn import datasets 
import matplotlib.pyplot as plt 
from myConvexHull import convexHull

def pickData():
    """Get user chosen data and columns out of 3 available datasets"""
    
    # print list of available datasets
    print("List of available datasets")
    print("1. CSV File")
    print("2. Iris")
    print("3. Wine")
    print("4. Breast Cancer")
    choice = int(input("Enter dataset number: "))

    # initialize csv dataset
    if (choice == 1):
        print("--------------------------------------------------------")
        print("[Make sure CSV file is in 'test' folder & has target]")
        datasetname = input("Enter filename (<FILENAME>.csv): ")
        try:
            df = pd.read_csv("./test/" + datasetname)
        except:
            print("File not found")
            return
        # check if file has target
        if (('target' not in df) and ('Target' not in df)):
            print("Unable to process file (no target found)")
            return
        # initialize target
        target = (df.target.unique())
    # initialize sklearn dataset
    else:
        if (choice == 2):
            data = datasets.load_iris()
            datasetname = "Iris"
        elif (choice == 3):
            data = datasets.load_wine()
            datasetname = "Wine"
        else:
            data = datasets.load_breast_cancer()
            datasetname = "Breast Cancer"
        df = pd.DataFrame(data.data, columns=data.feature_names)
        # initialize target
        df['Target'] = pd.DataFrame(data.target)
        target = data.target_names

    # initialize column choices
    print("--------------------------------------------------------")
    print("List of available columns in", datasetname, "dataset")
    i = 1
    for col in df.columns:
        if (col == 'target' or col == 'Target'):
            continue
        print(str(i) + ". " + str(col))
        i += 1
    print("Enter two column numbers to test linear separability")
    x = int(input("First column number: ")) - 1
    y = int(input("Second column number: ")) - 1
    title = (df.columns[x] + " vs " + df.columns[y])

    # process data through acquired choices
    processData(target, df, x, y, title)

def processData(target, df, x, y, title):
    """Visualize linear separability dataset test"""

    # initialize plot and color
    plt.figure(figsize = (10, 6))
    colors = ['b','r','g']
    plt.title(title)
    plt.xlabel(df.columns[x])
    plt.ylabel(df.columns[y])

    # plot convex hull per target
    for i in range(len(target)):
        try:
            bucket = df[df['Target'] == i]
        except:
            bucket = df[df['target'] == i]
        bucket = bucket.iloc[:,[x,y]].values
        hull = convexHull(bucket)
        plt.scatter(bucket[:, 0], bucket[:, 1], label=target[i])
        for simplex in hull:
            plt.plot([simplex[0][0], simplex[1][0]], [simplex[0][1], simplex[1][1]], colors[i % 3])
    plt.legend()
    plt.show()

pickData()
