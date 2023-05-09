#!/bin/bash


while read url; do
    echo "Getting $url"
    wget -r -k -l 4 -H -nc --random-wait -e robots=off "$url"
done < seed.txt
