#!/bin/bash

lines=$(ls ../sequences)

while read -r line; do
  line=$(echo ${line} | sed 's/-.*$//')
  echo "adding ${line} to file"
  grep "${line}" data_file.csv >> new_data_file.csv
done <<< "${lines}"
