#!/usr/bin/env python
import riak
from kafka import KafkaConsumer
from pymongo import MongoClient
from json import loads

port = 8087
bucket = "patients"
topic = "mongo.test.patients"

print("Connecting to Riak DB at port %s") % (port)
client = riak.RiakClient(pb_port=port, protocol='pbc')

print("Connecting to kafka")
consumer = KafkaConsumer(topic, bootstrap_servers=['localhost:9092'])


for message in consumer:
    message = message.value

    print('{} received'.format(message))
