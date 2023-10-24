import numpy as np

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

# Desired simulation sample size
N = 1000

def generateW():
    w = 0  # w is the total time spent calling
    completedAttempts = 0
    done = False
    while not done and completedAttempts < 4:
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
                done = True
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

def generateSample():
    output = []
    for i in range(N):
        w = generateW()
        output.append(w)
    return output


def generateAndPrintEstimates(sample):
    
    # Sample Distribution Basics
    sortedSample = sorted(sample)
    mean = np.mean(sortedSample)
    quartile1 = sortedSample[249]
    quartile2 = sortedSample[499]
    quartile3 = sortedSample[749]
    print(f'''Mean: {mean}\n1st Quartile: {quartile1}\nMedian: {quartile2}\n3rd Quartile: {quartile3}''')

    # Probabilities of events P[W <= eventCutoff]
    # TODO: Tail indicators TBD
    w5 = 60
    w6 = 70
    w7 = 80
    eventCutoffs= [ 15, 20, 30, 40, w5, w6, w7 ] # set cutoffs
    numbers_array = np.array(sortedSample)  # prep array
    for cutoff in eventCutoffs: 
        # calculate
        frequency = np.sum(numbers_array <= cutoff)
        probability = frequency / 1000
        # print
        print(f"P[W<{cutoff}] = {probability}")


def main():
    sample = generateSample()
    generateAndPrintEstimates(sample)


if __name__ == "__main__":
    main()
        






