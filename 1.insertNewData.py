#!/usr/bin/env python
import riak
import datetime
from faker import Factory

fake = Factory.create('en_UK')

myClient = riak.RiakClient(pb_port=8087, protocol='pbc')
user_bucket = myClient.bucket('patients')

numberOfRecords = 10

for i in range(numberOfRecords):
    # Fake customer info
    addr=fake.address()
    addrstreet=addr.split("\n")
    addrcity=addrstreet[1]

    # We're creating the user data & keying off their username.
    new_user = user_bucket.new(fake.uuid4(), data={
        "name":fake.name(),
        "nino":fake.ssn(),
        "dob": fake.date(),
        "gp":fake.name(),
        "job":fake.job(),
        "smoker": fake.boolean(chance_of_getting_true=14),
        "lastUpdated": datetime.datetime.utcnow().isoformat(),
        "phone":[
                {"home":fake.phone_number()},
                {"cell":fake.phone_number()}
        ],
        "address":{
                    "street":addrstreet[0],
                    "city":addrcity
        }
    })
    # Note that the user hasn't been stored in Riak yet.
    new_user.store()