#!/bin/bash

set -eou 
reference=$1
query=$2
mkdir -p $reference
echo "1.extract psl"

halSynteny out.hal /dev/stdout --queryGenome $query --targetGenome $reference \
| pslPosTarget stdin $reference/$reference.$query.psl
echo "2.chainNetting"
axtChain -psl -linearGap=loose $reference/$reference.$query.psl ../01.data/01.genome/2bit/$reference.2bit ../01.data/01.genom
 | chainSort stdin  $reference/$reference.$query.raw.chain
chainCleaner $reference/$reference.$query.raw.chain ../01.data/01.genome/2bit/$reference.2bit ../01.data/01.genome/2bit/$quererence.$query.clean.bed -linearGap=loose -tSizes=../01.data/01.genome/2bit/$reference.size -qSizes=../01.data/01.genome/2bit/
chainPreNet $reference/$reference.$query.clean.chain ../01.data/01.genome/2bit/$reference.size ../01.data/01.genome/2bit/$que
 | chainNet stdin  ../01.data/01.genome/2bit/$reference.size ../01.data/01.genome/2bit/$query.size stdout /dev/null \
 | netSyntenic stdin $reference/$reference.$query.net

echo "get RBH"
netChainSubset $reference/$reference.$query.net $reference/$reference.$query.clean.chain $reference/$reference.$query.best.ch

chainStitchId $reference/$reference.$query.best.chain stdout \
 | chainSwap stdin stdout \
 | chainSort stdin $reference/$query.$reference.tBest.chain

chainPreNet $reference/$query.$reference.tBest.chain ../01.data/01.genome/2bit/$query.size ../01.data/01.genome/2bit/$referen
 | chainNet stdin  ../01.data/01.genome/2bit/$query.size ../01.data/01.genome/2bit/$reference.size stdout /dev/null \
 | netSyntenic stdin $reference/$query.$reference.rbest.net

netChainSubset $reference/$query.$reference.rbest.net $reference/$query.$reference.tBest.chain stdout \
 |  chainStitchId stdin stdout \
 | gzip -c > $reference/$query.$reference.rBest.chain.gz

chainSwap $reference/$query.$reference.rBest.chain.gz