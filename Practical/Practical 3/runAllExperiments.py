from simpleBot3 import *
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind


def runSetOfExperiments(numberOfRuns, numberOfBots, movement_method):
    dirtCollectedList = []
    for _ in range(numberOfRuns):
        dirtCollectedList.append(main(numberOfBots, movement_method))
    return dirtCollectedList


def runExperimentsWithDifferentParameters():
    resultsTable = {}
    for numberOfBots in range(1, 6):
        for movement_method in ['Wandering', 'aStar']:
            dirtCollected = runSetOfExperiments(2, numberOfBots, movement_method)
            resultsTable["robots: " + str(numberOfBots) + " " + movement_method + " Method"] = dirtCollected
    results = pd.DataFrame(resultsTable)
    print(results)
    results.to_excel("data.xlsx")
    print(ttest_ind(results["robots: 1"], results["robots: 2"]))
    print(results.mean(axis=0))
    results.boxplot(grid=False)
    plt.show()


runExperimentsWithDifferentParameters()
