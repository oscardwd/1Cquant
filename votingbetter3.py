import numpy as np
import pandas as pd
import random as rng
import matplotlib.pyplot as plt
import seaborn as sns
import warnings


warnings.filterwarnings("ignore")

# dictates whether party positions will be entirely random or assigned 'slots' on a spectrum from 0 to 1
ptype = input("Random or assigned parties? (r, a)") 

# generates the party belief starting positions
def pclump(party):
    if ptype == 'r':
        if party == 'green':
            partyclump = rng.uniform(0, 1)
        if party == 'red': 
            partyclump = rng.uniform(0, 1)
        if party == 'blue':
            partyclump = rng.uniform(0, 1)
        if party == 'purple':
            partyclump = rng.uniform(0, 1)
        if party == 'yellow':
            partyclump = rng.uniform(0, 1)
        return partyclump
    if ptype == 'a':
        if party == 'green':
            partyclump = rng.uniform(0.8, 1)
        if party == 'red': 
            partyclump = rng.uniform(0.6, 0.8)
        if party == 'blue':
            partyclump = rng.uniform(0.4, 0.6)
        if party == 'purple':
            partyclump = rng.uniform(0.2, 0.4)
        if party == 'yellow':
            partyclump = rng.uniform(0, 0.2)
        return partyclump

# calls the pclump function and assigns the values to a dataframe of party beliefs
d = {'Parties': ['green', 'red', 'blue', 'purple', 'yellow'], 
     'belief1': [pclump('green'), pclump('red'), pclump('blue'), pclump('purple'), pclump('yellow')], 
     'belief2': [pclump('green'), pclump('red'), pclump('blue'), pclump('purple'), pclump('yellow')], 
     'belief3': [pclump('green'), pclump('red'), pclump('blue'), pclump('purple'), pclump('yellow')],
     'belief4': [pclump('green'), pclump('red'), pclump('blue'), pclump('purple'), pclump('yellow')],
     'belief5': [pclump('green'), pclump('red'), pclump('blue'), pclump('purple'), pclump('yellow')],
    }
parties = pd.DataFrame(data = d)
parties.set_index('Parties', inplace=True)

# generates 2 sides of 'clumps' for voters - one on one side of the spectrum and one on another
def clumpinggen():
    global highclump
    global lowclump
    highclump = rng.uniform(0.5, 1)
    lowclump = rng.uniform(0, 0.5)

# generates 5 beliefs in a 1D array with a normal distribution from high/lowclump
def clumping():
    clumpdecide = rng.randint(0, 1)
    if clumpdecide == 0:
        clump = np.random.normal(highclump, 0.3, size=(1, 5))
    if clumpdecide == 1:
        clump = np.random.normal(lowclump, 0.3, size=(1, 5))
    np.clip(clump, 0, 1, out=clump)
    return clump

# creates a voter either with random values or with the assigned high/lowclump
def genvoter(voterno):
    if ptype == 'r':
        g1 = rng.random()
        g2 = rng.random()
        g3 = rng.random()
        g4 = rng.random()
        g5 = rng.random()
        newvoter = np.array([g1, g2, g3, g4, g5])
        return newvoter
    if ptype == 'a':
        newvoter = np.array(clumping())
        gvupdown = rng.randint(0, 1)
        chaos = rng.uniform(0, 0.1) # adds an extra degree of unpredictability and adds or subtracts to 
                                    # a voter's belief
        if gvupdown == 0:
            newvoter = newvoter + chaos
        if gvupdown == 1:
            newvoter = newvoter - chaos
        np.clip(newvoter, 0, 1, out=newvoter)
        return newvoter

# creates the result dataframe
result = pd.DataFrame(columns=['gredis','reddis','bludis','purdis','yeldis','1c','2c', '3c'])

def knnvoterabs(selvoter, result):
    # finds the absolute distance between the voter's position and the parties' positions
    gredis = np.sum(np.abs((parties.iloc[0, :].to_numpy() - selvoter)))
    reddis = np.sum(np.abs((parties.iloc[1, :].to_numpy() - selvoter)))
    bludis = np.sum(np.abs((parties.iloc[2, :].to_numpy() - selvoter)))
    purdis = np.sum(np.abs((parties.iloc[3, :].to_numpy() - selvoter)))
    yeldis = np.sum(np.abs((parties.iloc[4, :].to_numpy() - selvoter)))
    # creates a dict with the distances between the voter and parties
    newdises = {"gredis": gredis, "reddis": reddis, "bludis": bludis, "purdis": purdis, "yeldis": yeldis}
    # sorts these distances into a list from small to large
    sortedchoice = sorted(newdises.items(), key=lambda x: x[1])
    # creates dict entries with the voter's 1st, 2nd and 3rd choices
    newdises['1c'] = sortedchoice[0][0]
    newdises['2c'] = sortedchoice[1][0]
    newdises['3c'] = sortedchoice[2][0]
    # concatenates these choices and distances into a new dataframe
    result = pd.concat([result, pd.DataFrame([newdises])], ignore_index=True)
    return result

# creates a dataframe to contain all elections ran
pastelections = pd.DataFrame(columns=['winner', 'wastedvotes', 'wastedprop (%)', 'green', 'red', 'blue', 'purple', 'yellow'])

# inputs the parameters for the simulation
electype = input("What type of election model would you like to run? (fptp, weighted)")
voterno = int(input("How many voters per constituency?"))
consize = int(input("How many constituencies?"))
electionno = int(input("How many elections?"))

# creates a series with all of the constituency results
constres = pd.Series()
result = pd.DataFrame(columns=['gredis','reddis','bludis','purdis','yeldis','1c','2c', '3c'])

# sets a for loop for the amount of election iterations
for y in range(electionno):
    wastedvotes = 0

    # reshuffles the party positions before each election
    d = {'Parties': ['green', 'red', 'blue', 'purple', 'yellow' ], 
     'belief1': [pclump('green'), pclump('red'), pclump('blue'), pclump('purple'), pclump('yellow')], 
     'belief2': [pclump('green'), pclump('red'), pclump('blue'), pclump('purple'), pclump('yellow')], 
     'belief3': [pclump('green'), pclump('red'), pclump('blue'), pclump('purple'), pclump('yellow')],
     'belief4': [pclump('green'), pclump('red'), pclump('blue'), pclump('purple'), pclump('yellow')],
     'belief5': [pclump('green'), pclump('red'), pclump('blue'), pclump('purple'), pclump('yellow')],
    }
    parties = pd.DataFrame(data = d)
    parties.set_index('Parties', inplace=True)

    # sets a for loop for the amount of constituencies generated
    for x in range(consize):
        result = pd.DataFrame(columns=['gredis','reddis','bludis','purdis','yeldis','1c','2c', '3c'])
        clumpinggen()
        # creates a list of belief arrays for each voter
        i=0
        arrays = [genvoter(i) for i in range(voterno)]
        # stacks the arrays into one array
        voterarr = np.vstack(tuple(arrays))
        # turns the array into a dataframe
        genvoterdf = pd.DataFrame(voterarr) 
        genvoterdf.rename(columns={0: "belief1", 1: "belief2", 2: "belief3", 3: "belief4", 4: "belief5"}, inplace=True)

        i=0
        for i in range(voterno):
            # grabs the i-th voter and assigns to selvoter
            selvoter = voterarr[[i], :]
            # feeds the selvoter and previous results into the K-nearest neighbours distance finding function
            result = knnvoterabs(selvoter, result)
        result.replace({'gredis': 'green', 'reddis': 'red', 'bludis': 'blue', 'purdis': 'purple', 'yeldis': 'yellow'}, inplace=True)

        if electype == "fptp":
            # adds the current constituency result to the dataframe containing all the results for one election
            constres.loc[x] = result["1c"].value_counts().index[0]
            # calculates the number of voters that didn't get their 1st, 2nd or 3rd choice
            newwastedvotes = len(result[(result['1c'] != constres.loc[x]) & (result['2c'] != constres.loc[x]) & (result['3c'] != constres.loc[x])])
            wastedvotes = wastedvotes + newwastedvotes
        elif electype == "weighted":
            # same as above process but adds the weighted results rather than just the 1st choice
            weightedres = (result["1c"].value_counts() * 3) + (result["2c"].value_counts() * 2) + (result["3c"].value_counts())
            constres.loc[x] = weightedres.idxmax()
            newwastedvotes = len(result[(result['1c'] != constres.loc[x]) & (result['2c'] != constres.loc[x]) & (result['3c'] != constres.loc[x])])
            wastedvotes = wastedvotes + newwastedvotes
        print(result)
        
    # collates the constituency results into one election result
    electresult = constres.value_counts()#
    # places the result in a df with all other results
    pastelections.loc[y] = electresult
    print(electresult)
    # assigns the winner, wasted votes and proportion of wasted votes
    pastelections['winner'].loc[y] = electresult.index[0]
    pastelections['wastedvotes'].loc[y] = wastedvotes
    pastelections['wastedprop (%)'].loc[y] = (wastedvotes / (voterno * consize)) * 100
print(pastelections)

# saves the results as a CSV
try:
    pastelections.to_csv('aord.csv', index=False)
    print("CSV saved successfully")
except Exception as e:
    print("Error saving CSV:", e)