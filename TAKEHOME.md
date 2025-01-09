## Approach
It took me about an hour a day over a couple of days to arrive at this solution. The bulk of this time was decipering the index files and how the URLs contain encoded information about the in network rate files. I ascertained from utilizing the Anthem EIN lookup that a part of the URL encodes the state in which those in network files relate to as well as that the description for the file location objects is important as only the value of "In-Network Negotiated Rates Files" relates to actual in network rate files while all others seem to relate to "out of area" rate files. The script takes a stream processing approach of simply reading the file in and writing it out to another file as this approach has the least amount of resource requirements and as long as there is enough storage on the device it should complete successfully. I avoided maintaining the list of URLs in memory as this could become a bottleneck due to the size of the file.

## Setup
In order to run the script I have provided a Dockerfile that will build an image that will pull down the requisite data as well as contain the script.

### Build instructions
```
# Build docker file, execute in root directory of repo.
cd <to root directory>
docker build -t indexFileParser:latest .
```

### Execution Instructions
```

docker run --rm -v ${}
```

### Execution Time
From running the script locally it takes approximately 25 minutes to complete parsing the file on a relatively underpowered laptop.