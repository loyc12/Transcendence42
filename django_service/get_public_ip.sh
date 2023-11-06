#!/bin/sh
OUTPUT_FILE=$1
echo $OUTPUT_FILE
curl -X GET -fsSL -m 1 'https://ident.me' > $OUTPUT_FILE