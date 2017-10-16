#!/bin/bash

if [ -z "${1}" ]; then
	echo "provide a class name"
	exit 1
fi

class=${1}
videos=$(grep ${1} kinetics_train.csv)

iter=1
while read -r video; do
	IFS=',' read -r -a varr <<< "${video}"
	name="ytdl/${class}/${iter}.mp4"
	url="http://youtube.com/watch?v=${varr[1]}"
	opt="bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4"
	youtube-dl -f "${opt}" "${url}" -o "${name}"
	ffmpeg -y -i "${name}" \
	       -ss "${varr[2]}" \
	       -t 10 \
	       "ytdl/${class}/clip${iter}.wmv"
	rm "${name}"
	iter=$(expr $iter + 1)
done <<< "${videos}"
