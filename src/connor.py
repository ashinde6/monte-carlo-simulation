import math

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
    w = 0
    completedAttempts = 0
    done = False
    while not done or completedAttempts < 4:
        w += INITIATE_CALL_TIME
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
            if x < 25:
                w += timeToAnswer + END_CALL_TIME
                done = True
            else:
                w += 25 + END_CALL_TIME
                completedAttempts += 1
    return w


def inverseCDF(u):
    output = 0
    if u >= 0 and u < 1:
        output = -12 * math.log(1-u)
    return output
        






