from math import pow
def power(base , exp):
    return pow(base,exp)

def avergae(listed):
    avg=0
    for item in listed:
        avg+=item

    return avg/len(listed)
    