# SEA-final-project
Building up movie seach engine plus customized recommendation system

#tomatoCrawler
![alt tag](https://drive.google.com/file/d/0BzG5zLRRrgKwYWJUUHBsNmtDRUk/view?usp=sharing)

Will fetch rotten tomato website and save the following pickles:
./constants/Movie_dict and ./constants/Review_dict
Now we have:
- 250 movie to search
- 1718 movieIDs returned

#File System module Usage
##Distributed dictionary object
```python
from fs import DisTable

#Creating an object
a = DisTable()
# or
b = DisTable({ 1: 'a', 2: 'b', 3: 'c'})

#Set a key-value pair
a[1] = 'a'
a[2] = 'b'
#Get a value with key
a[1]
#returns 'a'

#Pop operation
a.pop(1)
#returns 'a' and remove (1, 'a') from dictionary

#hasKey operation
a.hasKey(2)
#returns True
a.hasKey(1)
#returns False

#Length property
a.length
#returns 1

#Pretty print of dictionary
print a
#1
#   a
'''
key1
  value1
  value2
  ...
key2
  value1
  value2
  ...
'''
```

##Distributed List
```python
from fs import DisList

#Creating an object
a = DisList()
# or
b = DisList([1, 2, 3, 4])

#Append/Extend a value into list
a.append(1)
a.append(2)
a.extend(3)
a.extend(4)

#Get a value given position
a[0]
#returns 1
a[1]
#returns 2

#Update value to given position
a[1] = 3
print a
#[ 1 3 3 4 ]

#Remove value from list
a.remove(1)
print a
#[ 3 3 4 ]
a.remove(3, globl=True)
print a
#[ 4 ]

#Pop operation
a.pop(1)
#returns 'a' and remove (1, 'a') from dictionary

#Length property
a.length
#returns 1
```
