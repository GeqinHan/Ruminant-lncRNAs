#!/bin/bash

cactus-hal2maf \
    ./js \
    01.input.hal \
    01.output-chr1.sheep_ref.maf.gz \
    --refGenome sheep_chr1 \
    --chunkSize 500000 \
    --noAncestors \
    --batchCores 32 \
    --filterGapCausingDupes \
    --targetGenomes camel,pig,xilu,pronghorn,giraffe,muskdeer,cattle,sheep,goat,mhl,XL,hippo,killer_whale,tapir