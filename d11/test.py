from solution import Stone, blink

t1 = [Stone(125), Stone(17)]
print(t1)

for i in range(6):
    t1 = blink(t1)
    print(f"Round {i+1}: {t1}")
