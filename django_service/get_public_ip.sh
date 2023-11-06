#!/bin/sh
OUTPUT_FILE=$1
echo $OUTPUT_FILE
curl -X GET -fsSL 'https://ident.me' > $OUTPUT_FILE