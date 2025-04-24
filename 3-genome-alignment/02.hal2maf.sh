#!/bin/bash

cactus-hal2maf \
    ./js \
    01.input.hal \
    02.output_sheep_ref_chr1.maf \
    --refGenome sheep_chr1 \
    --chunkSize 500000 \
    --noAncestors \
    --batchCores 32 \
    --filterGapCausingDupes \
    --targetGenomes camel,pig,lesser_mouse_deer,pronghorn,giraffe,forest_musk_deer,cattle,sheep,goat,sika_deer,reindeer,hippo,killer_whale,tapir