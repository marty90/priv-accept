#!/bin/bash
# Usage: ./split_urls.sh <url_file> <number_of_chunks>

# Check if a file name was provided as an argument
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <url_file> <number_of_chunks>"
    exit 1
fi

# Assign arguments to variables
URL_FILE=$1
NUM_CHUNKS=$2

# Check if the specified file exists
if [ ! -f "$URL_FILE" ]; then
    echo "The file $URL_FILE does not exist."
    exit 1
fi

# Create a directory for URL chunks if it doesn't exist
URL_CHUNKS_DIR="$(pwd)/url_chunks"
mkdir -p "$URL_CHUNKS_DIR"

# Clean the url_chunks directory
rm -f "${URL_CHUNKS_DIR:?}"/*

# Calculate the number of lines per chunk
TOTAL_LINES=$(wc -l < "$URL_FILE")
(( LINES_PER_CHUNK = (TOTAL_LINES + NUM_CHUNKS - 1) / NUM_CHUNKS ))
echo "Total lines: $TOTAL_LINES"
echo "Each chunk contains $LINES_PER_CHUNK lines."

# Split the file into chunks and store them in the url_chunks directory
split -l "$LINES_PER_CHUNK" "$URL_FILE" "${URL_CHUNKS_DIR}/url_chunk_"

# Rename files to have a numeric suffix
a=0
for file in "${URL_CHUNKS_DIR}/url_chunk_"*
do
   mv "$file" "${URL_CHUNKS_DIR}/url_chunk_$a"
   let a++
done

echo "Split $URL_FILE into $NUM_CHUNKS chunks."