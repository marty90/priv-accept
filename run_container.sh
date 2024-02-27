#!/bin/bash

# Usage: ./run_containers.sh <docker_image_name> <url_file> <number_of_chunks>

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <docker_image_name> <url_file> <number_of_chunks>"
    exit 1
fi

DOCKER_IMAGE=$1
URL_FILE=$2
NUM_CHUNKS=$3

docker pull $DOCKER_IMAGE
./split_urls.sh $URL_FILE $NUM_CHUNKS

for i in $(seq 0 $((NUM_CHUNKS-1)))
do
   chunk_file_path="/opt/priv-accept/url_chunks/url_chunk_$i"
   docker run -d -v "$(pwd)/url_chunks:/opt/priv-accept/url_chunks" -v "$(pwd)/output:/opt/priv-accept/output" $DOCKER_IMAGE /opt/priv-accept/run_priv.sh $chunk_file_path $i
done

echo "Launched $NUM_CHUNKS containers."