#!/usr/bin/env python
import riak
import json
from datetime import datetime
import time

port=8087
bucket="patients"

print("Connecting to Riak DB at port %s") % (port)
client = riak.RiakClient(pb_port=port, protocol='pbc')

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
                print "Key %s" % (result[0])
                print "Value\n" +json.dumps(result[1], sort_keys=True, indent=4)
                lastUpdatedValue = datetime.strptime(result[1]['lastUpdated'],"%Y-%m-%dT%H:%M:%S.%f")
                if lastUpdatedValue > lastUpdated:
                    lastUpdated = lastUpdatedValue
    
        wait = 5
        print("Waiting %ssec") % (wait)
        time.sleep(wait)

getLatestData(lastUpdated)