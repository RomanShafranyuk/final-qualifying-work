import math


def calculate_probability(q:float, m:int):
    p = 1.0 - q
    l = m * (q/p)
    P = 1.0
    for k in range(m):
        P -= l**k * math.exp(-l) * (1- math.pow(q/p, m-k)) / math.factorial(k)
    
    return P

if __name__ == "__main__":
    results = {}
    for q in range(1, 6, 1):
        for m in range(1, 11):
            if m == 1:
                results[q/10] = []
            results[q/10].append(calculate_probability(q/10,m))
    print(results) 
    



