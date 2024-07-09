#!/bin/bash

# Initialize the configuration servers
docker exec -it mongocfg1 bash -c 'echo "rs.initiate({_id: \"mongors1conf\", configsvr: true, members: [{_id: 0, host: \"mongocfg1\"}, {_id: 1, host: \"mongocfg2\"}, {_id: 2, host: \"mongocfg3\"}]})" | mongosh'

# Check the status of the configuration servers
docker exec -it mongocfg1 bash -c 'echo "rs.status()" | mongosh'

# Initialize the first shard replica set
docker exec -it mongors1n1 bash -c 'echo "rs.initiate({_id: \"mongors1\", members: [{_id: 0, host: \"mongors1n1\"}, {_id: 1, host: \"mongors1n2\"}, {_id: 2, host: \"mongors1n3\"}]})" | mongosh'

# Check the status of the first shard
docker exec -it mongors1n1 bash -c 'echo "rs.status()" | mongosh'

# Add the first shard to the router
docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors1/mongors1n1\")" | mongosh'

# Initialize the second shard replica set
docker exec -it mongors2n1 bash -c 'echo "rs.initiate({_id: \"mongors2\", members: [{_id: 0, host: \"mongors2n1\"}, {_id: 1, host: \"mongors2n2\"}, {_id: 2, host: \"mongors2n3\"}]})" | mongosh'

# Add the second shard to the router
docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors2/mongors2n1\")" | mongosh'

# Check the status of the cluster
docker exec -it mongos1 bash -c 'echo "sh.status()" | mongosh'

# Create a test database
docker exec -it mongors1n1 bash -c 'echo "use someDb" | mongosh'

# Enable sharding on the test database
docker exec -it mongos1 bash -c 'echo "sh.enableSharding(\"someDb\")" | mongosh'

# Create a test collection
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"someDb.someCollection\")" | mongosh'

# Shard the collection on someField
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"someDb.someCollection\", {\"someField\": \"hashed\"})" | mongosh'

echo "MongoDB cluster setup complete."

