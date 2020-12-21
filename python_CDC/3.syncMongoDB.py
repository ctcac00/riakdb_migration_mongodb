#!/usr/bin/env python
import sys
import csv
import json
import pymongo

import riak
import json
from datetime import datetime
import time

port=8087
bucket="patients"

print("Connecting to Riak DB at port %s") % (port)
client = riak.RiakClient(pb_port=port, protocol='pbc')

mongodb_uri = "mongodb://localhost:27017"
print("Connecting to MongoDB at uri %s") % (mongodb_uri)
myclient = pymongo.MongoClient(mongodb_uri)
mydb = myclient["health"]
mycol = mydb["patients"]
mycol.drop()

lastUpdated = datetime(2020, 1, 1)

def getLatestData(lastUpdated):
    while True:
        print("Getting latest data from bucket %s since %s") % (bucket,lastUpdated.isoformat())
        mapReduce = "function(v) { var data = JSON.parse(v.values[0].data); if(data.lastUpdated > '%s') { return [[v.key, data]]; } return []; }" % (lastUpdated.isoformat())
        query = client.add(bucket)
        query.map(mapReduce)
        resultSet = query.run()

        if not resultSet:
            print("No new data...")
        else:
            for result in resultSet:
                key = result[0]
                data = result[1]
                print "Key %s" % (key)
                print "Value\n" +json.dumps(data, sort_keys=True, indent=4)

                data['_id'] = key
                mycol.insert_one(data)

                lastUpdatedValue = datetime.strptime(data['lastUpdated'],"%Y-%m-%dT%H:%M:%S.%f")
                if lastUpdatedValue > lastUpdated:
                    lastUpdated = lastUpdatedValue
    
        wait = 5
        print("Waiting %ssec") % (wait)
        time.sleep(wait)

getLatestData(lastUpdated)