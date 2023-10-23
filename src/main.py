a = 24693
x0 = 1000
c = 3517
K = pow(2, 17)


def random_number(n):
    values = []
    values.append(x0)

    decimals = []

    x = 0
    while x < n:
        xi = generateX(values[x])
        values.append(xi)

        ui = generateDecimal(xi)
        decimals.append(ui)

        print(ui)

        x = x+1

def generateX(x):
    return (x*a + c) % K

def generateDecimal(xi):
    return xi/K

def main():
    random_number(3)
    

