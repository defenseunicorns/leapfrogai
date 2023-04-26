#!/bin/bash


while read url; do
    echo "Getting $url"
    wget -r "$url"
done < seed.txt
