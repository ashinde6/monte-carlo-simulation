import numpy as np
import matplotlib.pyplot as plt

# Call Action Times
INITIATE_CALL_TIME = 6
BUSY_TIME = 3
NOT_AVAILABLE_TIME = 25
END_CALL_TIME = 1

# Random Number Generator Parameters
SEED = 1000
MULTIPLIER = 24693
INCREMENT = 3517
MODULUS = 2**17

# Case Boundaries
BUSY_BOUND = 0.2
NOT_AVAILABLE_BOUND = BUSY_BOUND + 0.3

# Global Tracker for Previous x (randomly generated number)
x = SEED

def generateW():
    w = 0  # w is the total time spent calling
    completedAttempts = 0
    callAnswered = False
    while not callAnswered and completedAttempts < 4:
        w += INITIATE_CALL_TIME
        global x
        x = getRandNum(x)
        randCase = toDecimal(x)
        if randCase < BUSY_BOUND:
            w += BUSY_TIME + END_CALL_TIME
            completedAttempts += 1
        elif randCase < NOT_AVAILABLE_BOUND:
            w += NOT_AVAILABLE_TIME + END_CALL_TIME
            completedAttempts += 1
        else:  # this is the AVAILABLE case
            x = getRandNum(x)
            u = toDecimal(x)
            timeToAnswer = inverseCDF(u)
            if timeToAnswer < 25:
                w += timeToAnswer + END_CALL_TIME
                callAnswered = True
            else:
                w += 25 + END_CALL_TIME
                completedAttempts += 1
    return w


def getRandNum(previous_random_number):
    return (previous_random_number * MULTIPLIER + INCREMENT) % MODULUS


def toDecimal(random_number):
    decimal = round(random_number / MODULUS, 4)
    # if decimal >= 1:
    #     raise Exception("Decimal representation of the given random number %f is greater than or equal to 1", decimal)
    # elif decimal < 0:
    #     raise Exception("Decimal representation of the given random number %f is less than 0", decimal)
    return round(random_number / MODULUS, 4)


def inverseCDF(u):
    output = 0
    if u >= 0 and u < 1:
        output = -12 * np.log(1-u)
    return output


def generateSample(n):
    output = []
    for i in range(n):
        w = generateW()
        output.append(w)
    return output


def generateEstimates(sample):

    # Sample Distribution Basics
    estimates = {}
    sortedSample = sorted(sample)
    estimates["mean"] = round(np.mean(sortedSample), 2)
    estimates["quartile1"] = round(sortedSample[249], 2)
    estimates["median"] = round(sortedSample[499], 2)
    estimates["quartile3"] = round(sortedSample[749], 2)

    # Probabilities of events P[W <= eventCutoff]
    cutoffsOnetoThree = [15, 20, 30]  # set cutoffs
    for cutoff in cutoffsOnetoThree:
        frequency = len([x for x in sample if x <=cutoff])
        probability = frequency / 1000
        estimates[f"P[W<={cutoff}]"] = probability
    
    # Probabilities of events P[W <= eventCutoff]
    w5 = 50
    w6 = 60
    w7 = 65
    cutoffsFourtoSeven = [40, w5, w6, w7]
    for cutoff in cutoffsFourtoSeven:
        frequency = len([x for x in sample if x >cutoff])
        probability = frequency / 1000
        estimates[f"P[W>{cutoff}]"] = probability
    

    return estimates


def printDict(dict):
    for key in dict:
        print(f"{key}: {dict[key]}")


def generateGraph(sample):
    histogram(sample)
    boxPlot(sample)
    CDF(sample)
    return

def histogram(sample):
    plt.figure()  # Create a new figure
    w = np.array(sample)
    plt.hist(w)
    plt.show(block=False)

    return

def boxPlot(sample):
    plt.figure()  # Create a new figure
    box_plot_data = [sample]
    plt.boxplot(box_plot_data, patch_artist=True)
    plt.show(block=False)

    return

def CDF(sample):
    plt.figure()  # Create a new figure
     # Step 1: Sort the data
    x = np.sort(sample)
    
    # Step 2: Calculate the cumulative frequency
    n = x.size
    y = np.arange(1, n+1) / n  # This gives the fraction or percent of data points below each value in x

    # Step 3: Plot the sorted values against their corresponding cumulative frequencies
    plt.plot(x, y, linewidth=2)

    # Manually created, rough-estimate line of best-fit
    x_func = np.linspace(7, 130, 500)
    y_func = 1- np.e**(-0.0275*(x_func - 7))
    plt.plot(x_func, y_func, color='red', linewidth=2)
    plt.grid(True)
    plt.show()

    return



def main():
    sample = generateSample(1000)
    print(sample[0:9])  # check first 10 entries just in case!
    printDict(generateEstimates(sample))
    generateGraph(sample)
    return


if __name__ == "__main__":
    main()
