# Scalability and Consistency
## BuildHunter Team
- Christopher Keinsley
- Jack Peterson
- Collin Moore
- Rahul Yarlagadda

## Neo4J

## Redis

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