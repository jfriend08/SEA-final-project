##File System Usage

###Example
```python
from fs import DisList, DisTable

#Build up DisTable on machine A
test = DisTable({1: 'a', 2: 'b', 3: [1, 2, 3, 4, {5: 'f', 6: 'g', 7: 'h'}]}, tableName='TEST')

#Use data from machine B
a = DisTable(tableName='TEST')
a[1]
#output: 'a'

#Fetch all data to local memory
#Machine A
test.fetch_all()
#output: {1: 'a', 2: 'b', 3: [1, 2, 3, 4, {5: 'f', 6: 'g', 7: 'h'}]}

#Machine B
a.fetch_all()
#output: {1: 'a', 2: 'b', 3: [1, 2, 3, 4, {5: 'f', 6: 'g', 7: 'h'}]}

```
