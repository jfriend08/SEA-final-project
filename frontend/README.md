## Frontend Server

# backend server info

create a json file "worker_info.json" into frontend/config and its content should be like:

```
{
  "classifier" : ["127.0.0.1:15001"],
  "search" : ["127.0.0.1:15002", "127.0.0.1:15003", "127.0.0.1:15004"],
  "recommand" : ["127.0.0.1:15005", "127.0.0.1:15006", "127.0.0.1:15007"]
}

```

# install google cloud sdk

https://cloud.google.com/sdk/#Quick_Start

```
$ curl https://sdk.cloud.google.com | bash

```

# start the frontend server

```
$ dev_appserver.py --host=localhost --port=8080 frontend

```

# will send three kinds of http request to our backend servers

```python

# to classifier

http://127.0.0.1:15001/predict?description=tracking+high

# to search engine 

http://127.0.0.1:15003/search?query=tracking+high&genre=%5B%27Comedy%27%2C+%27Drama%27%5D

# to recommand engine

http://127.0.0.1:15007/recommand?genre=%5B%27Comedy%27%2C+%27Drama%27%5D&user=158238155239231271481


```

