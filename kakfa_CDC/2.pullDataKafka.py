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
consumer = KafkaConsumer(
    topic,
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: loads(x.decode('utf-8')))


for message in consumer:
    message = message.value

    print('{} received'.format(message))
