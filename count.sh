#!/bin/bash

if [ $# -ne 4 ] ; then
	echo 'Syntax: count.sh QA QB QC PRIME'
	echo '  for the form <QA, QB, QC*PRIME>'
	exit 3
fi

fname="c_$1_$2_$3_$4"

echo "#define PRIME ${4}ll" > ${fname}.cpp
echo "#define QA ${1}ll" >> ${fname}.cpp
echo "#define QB ${2}ll" >> ${fname}.cpp
echo "#define QC ${3}ll" >> ${fname}.cpp
cat count.cpp >> ${fname}.cpp

g++ --std=c++11 -pthread -O3 -o ./${fname}.out ${fname}.cpp &&
./${fname}.out | tee ./${fname}.txt

