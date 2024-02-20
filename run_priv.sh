#!/bin/bash

# Ensure the script exits if any command fails
set -e

# Check if a file name was provided as an argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <url_file>"
    exit 1
fi

# Assign the first argument to FILENAME variable
FILENAME=$1

# Check if the specified file exists
if [ ! -f "$FILENAME" ]; then
    echo "The file $FILENAME does not exist."
    exit 1
fi

count=0
# Loop through each line in the specified file
while IFS= read -r url
do
    # Run priv-accept.py with each URL
    python /opt/priv-accept/priv-accept.py --url "$url" --outfile "output${count}.json" --docker
    ((count+=1))
    echo $url
    # sleep 60
done < "$FILENAME"

echo "Finished processing run_priv.sh."
sleep 10