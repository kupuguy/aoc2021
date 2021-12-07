input = "16,1,2,0,4,2,7,1,2,14"
input=open('../input/day7.txt').read().strip()
data = [int(n) for n in input.split(',')]

print(sum(data), len(data), sum(data)/len(data))

def triangle(n):
    return n*(n+1)//2

def cost(values, target):
    return sum(triangle(abs(v-target)) for v in values)

print(min(cost(data, n) for n in range(max(data))))
