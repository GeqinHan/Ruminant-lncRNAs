#!/bin/bash

PYPY_PATH=~/soft/pypy/pypy3.7-v7.3.3-linux64/bin/pypy
SCRIPT_PATH=02.input-changemaf2list.py
MAFFILE= 01.output-chr1.sheep_ref.maf.gz 
SPECIESFILE=02.input-specieslist
OUTFILE=02.output-chr1.sheep_ref.maf.list
SP1ADDL=cattle

$PYPY_PATH $SCRIPT_PATH --maffile $MAFFILE --speciesfile $SPECIESFILE --outfile $OUTFILE --sp1addlc $SP1ADDL