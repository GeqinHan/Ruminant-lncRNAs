#!/bin/bash

cactus-hal2maf \
    ./js \
    01.input.hal \
    02.output-chr1.sheep_ref.maf.gz \
    --refGenome sheep_chr1 \
    --chunkSize 500000 \
    --noAncestors \
    --batchCores 32 \
    --filterGapCausingDupes \
    --targetGenomes camel,pig,mouse-deer,pronghorn,giraffe,muskdeer,cattle,sheep,goat,sika deer,reindeer,hippo,killer_whale,tapir