from cs50 import get_float
from cs50 import get_int

m = get_float("Change owed: ")
while m < 0:
    m = get_float("Change owed: ")
coins = 0
money = m * 100
while (money >= 25):
    money -= 25
    coins += 1
while (money >= 10):
    money -= 10
    coins += 1
while (money >= 5):
    money -= 5
    coins += 1
while (money >= 1):
    money -= 1
    coins += 1
print(coins)