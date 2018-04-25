# Cassandra

## Setup
This will help you install and setup cassandra on ubuntu 16.04.

### Install Java
On every node that cassandra will be installed on you will need to install Java.  
You can install Java by running the following commands  
```
sudo apt-get update
sudo apt-get install openjdk-8-jdk
```
You can then check to make sure java is installed with
```
java -version
```

### Installation
Add the repository for Cassandra to every node
```
echo "deb http://debian.datastax.com/community stable main" | sudo tee -a /etc/apt/sources.list.d/datastax.community.list
```
Add the Cassandra repository keys to every node
```
curl -L https://debian.datastax.com/debian/repo_key | sudo apt-key add -
```

Update the repositories and install python support
```
sudo apt-get update
wget http://launchpadlibrarian.net/109052632/python-support_1.0.15_all.deb
sudo dpkg -i python-support_1.0.15_all.deb
```

Install Cassandra
```
sudo apt-get install dsc21=2.1.5-1 cassandra=2.1.5 cassandra-tools=2.1.5 -y
```

### Clustering
In order to setup Cassandra for clustering, first stop cassandra
```
sudo service cassandra stop
```
Then we can edit the Cassandra config file in `/etc/cassandra/cassandra.yaml` on every node
```
vim /etc/cassandra/cassandra.yaml
```
Find `-seeds:` and change the `"127.0.0.1"` to have a comma separated list of the ip addresses of all the nodes for the cluster  

In each nodes config file, find `listen_address` and set it to the ip address of that node. Then find the `rpc_address`and remove `localhost`, leaving it blank. Save all of the files.  

Restart Cassandra 
```
sudo service cassandra restart
```

If everything worked, you should be able to run 
```
sudo nodetool status
```
and see output similar to
```
Datacenter: datacenter1
=======================
Status=Up/Down
|/ State=Normal/Leaving/Joining/Moving
--  Address        Load       Tokens       Owns (effective)  Host ID                               Rack
UN  137.112.89.75  468.63 KiB  256          68.3%             e4059108-8bcf-4412-a4b7-0eb041e6ca20  rack1
UN  137.112.89.76  318.69 KiB  256          69.5%             60f1e39f-3898-4f60-87e5-99aff0a44545  rack1
UN  137.112.89.78  320.06 KiB  256          62.2%             5633afff-c470-4a97-b529-12733fe9a5b4  rack1
```

### Python Driver
Install the python driver
```
sudo -H pip install cassandra-driver
```

Export a variable to override bundled driver
```
export CQLSH_NO_BUNDLED=true
```

You should be able to connect using python by 
```
from cassandra.cluster import Cluster
cluster = Cluster(['<Node IP Address>'])
session = cluster.connect()
```
