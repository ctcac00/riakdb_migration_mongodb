# Instructions

## Dependecies

* Docker
* Python2.7

## Set up the virtual environment

* Run the [setup.sh](./setup.sh) script to set up a new virtual environment and install all the required dependencies

## Riak DB to MongoDB migration using a simple CDC tool

* Run [1.insertNewData.py](./1.insertNewData.py) to insert new data in Riak DB

* [Optional] Run [2.getLatestData.py](./2.getLatestData.py) to read data from Riak DB in 5sec intervals

* Run [3.syncMongoDB.py](./3.syncMongoDB.py) to read data from Riak DB and insert it into MongoDB, in 5sec intervals

## Tips and Tricks

You can connect to Riak Explorer at this [address](http://localhost:8098/admin/#/cluster/default/data)
