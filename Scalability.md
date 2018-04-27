# Scalability and Consistency
## BuildHunter Team
- Christopher Keinsley
- Jack Peterson
- Collin Moore
- Rahul Yarlagadda

## Neo4J

## Redis

### Scalability

#### Options

So redis supports both replication and sharding. There are several ways to implement sharding/partitioning in Redis. The first method is through range partitioning, where you store a certain range of data on particular nodes. The second is hash partitioning where you store a range of hashes on each node. The third and most appealing is query partitioning, in which the client can send a query to any node and the node will ensure the query is routed to the nodes with the data the query requires. The last option that sounds great is only available in Redis Cluster, which is not a free product. It allows for automated sharding of your data across the cluster. Replication is supported for free through Redis’s replication sets. This allows for multiple nodes to hold a replica of the database, which means if a load balancer is used the system can increase throughput for processing incoming requests there are more nodes to handle them.

#### Justification

We opted not to shard/partition our redis database because we only have 4 nodes and thought the benefits would not be as great since our system does not have different enough data to justify its necessity. Replication however seemed like a must for us, so that we can make more reads, which is primarily what our application does. We put it on two nodes only because Redis uses a ton of RAM so we did not want to limit some of our other nodes ability to perform.

### Consistency

#### Options

As far as consistency Redis offers replication sets using a Master-Slave architecture. Redis also uses snapshots and journaling to help with failover. If we examine the case where there is a single node, if the node goes down and reboots, the node will use the a snapshot or the journal as a recovery point. Any write requests that occured while the node was down will be lost. However, if there are multiple nodes, say in the case of a replication set, if a node goes down other than the master it will start from its last known state from either the snapshot or journalling or some combination depending on the configuration, and then communicates with the master node to ‘catch’ up to the current state of the data. They do this by having the Master node send all the writes its received after the most recent timestamp in the journal of the node that went down. If the Master node goes down then writes halt and the slave node will still be able to handle reads. There are ways to allow for writable slave nodes but this can get a bit complex and for the way we are using redis (primarily as a fast read mostly static data store) it does not make sense to use.

#### Justification

We chose to setup Redis in a replica set of two nodes, one master one slave. The main reason we did this is we don’t want our RAM to get totally filled on all of our nodes. We do not allow writes on the slave node and we use the default snapshotting and journalling configuration.

## Cassandra

### Scalability

Cassandra clusters operates in a ring. Each node in this ring are considered equals. There is no master node so there is no reason to worry about which node you are writing to or reading from. There is no single point of failure.  

Cassandra also supports the notion of a Data Center which options for both virtual and physical data centers. A cassandra cluster can span multiple data centers. Cassandra will allow us to query either the entire cluster or just the local data center. The benefit of this is that we can act like we are talking to the same cluster regardless of where we are, but only query the local nodes if we do not need the information from a data center in another country. This can greatly decrease the latency and amount of data needed to be transferred.  

Cassandra also supports replication out of the box. In cassandra these replicas are complete copies of the data such that if a single node goes down, the data can be retrieved from another node. These replica sets are customizable at the table/column family level. This customization allows for choosing how many copies of the data should exist and where on the rack they should be.  
Replication can be in single data center, across multiple data centers, or across different cloud providers. When replicating across multiple data centers, the number of copies in each data center is configurable.  

Scaling cassandra can be done in one of two ways, horizontally or vertically. Horizontal scaling in cassandra is adding more data centers. Vertical scaling is adding more nodes to a single data center. With cassandra there are no special cares that need to be taken when adding a new node, as it comes with a load balancer that will ensure the node takes on a portion of the current data-set when it comes online.  

Our choice was to setup cassandra in a four node ring where each node is on a different VM. This allows us to read or write from any node and ensures that as long one of our VMs is up that we can query from cassandra.  

### Consistency
Cassandra will be eventually consistent using asynchronous updating. When can write to any node which will propose the write request. The write request will be processed once a configured number of nodes accepts the write. Cassandra automatically handles a node going down through a self-healing process which includes scrubbing any corrupt data then reattaching the node to the ring just like a new node being added. This will 

### Justification

We picked this because we don't care