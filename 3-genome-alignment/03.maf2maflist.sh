#!/bin/bash

PYPY_PATH=~/soft/pypy/pypy3.7-v7.3.3-linux64/bin/pypy
SCRIPT_PATH=03.input_changemaf2list.py
MAFFILE= 02.output_sheep_ref_chr1.maf
SPECIESFILE=03.input_species_list
OUTFILE=03.output_sheep_ref_chr.maf.list
SP1ADDL=Cattle

$PYPY_PATH $SCRIPT_PATH --maffile $MAFFILE --speciesfile $SPECIESFILE --outfile $OUTFILE --sp1addlc $SP1ADDL