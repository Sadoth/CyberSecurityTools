#!/bin/bash

if test "$#" -ne 2; then
    echo "Usage : $0 src_url dst"
    exit 1
fi

wget -r -nH --cut-dirs=2 --no-parent $1 -P $2