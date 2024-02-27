#!/bin/bash

# # Ensure the script exits if any command fails
# set -e
# We don't want to exit if a single url can't run

# Check if a file name was provided as an argument
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <url_file> <UNIQUE_ID>"
    exit 1
fi

# Assign the first argument to FILENAME variable
FILENAME=$1

# Check if the specified file exists
if [ ! -f "$FILENAME" ]; then
    echo "The file $FILENAME does not exist."
    exit 1
fi
# Unique ID to identify the output file
UNIQUE_ID=$2
count=0
echo "Start processing run_priv.sh for chunk ${UNIQUE_ID}."
# Loop through each line in the specified file
while IFS= read -r url
do
    # Run priv-accept.py with each URL
    echo "Running ${url}."
    # python /opt/priv-accept/priv-accept.py --url "$url"
    python /opt/priv-accept/priv-accept.py --url "$url" --outfile "/opt/priv-accept/output/output_${UNIQUE_ID}_${count}.json" --docker --visit_internals
    ((count+=1))
    # echo $url
    # sleep 60
done < "$FILENAME"

echo "Finished processing run_priv.sh for chunk ${UNIQUE_ID}."
sleep 10