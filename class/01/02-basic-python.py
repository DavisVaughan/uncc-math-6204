import numpy as np

### Basic array
# Array from 0 to 3
x = np.array([0, 1, 2, 3])

x

### np.arange
# Starts at 0, ends at a number less than 4
# Includes the left side, does not include the right side
# increments by 1
y = np.arange(0, 4, 1)

y

#### Lists
# range in python3 generates an iterator type, not a list
z = list(range(4))
z

# list multiplication just extends the list
z * 2

### Array linspace
# Also create arrays using linspace (or arange)
# from 1 to 2 with 11 points total
lins = np.linspace(1.0, 2.0, 11)

# Array multiplication actually does elementwise multiplication
lins * 2

### For loop

# for loop with a range iterator
sum = 0
for i in range(11):
    sum = sum + i
    
sum = 0
for i in np.linspace(1, 10, 10):
    sum = sum + i

# or do the vector way
np.cumsum(list(range(11)))[-1]

# or just take a sum
np.sum(range(11))


