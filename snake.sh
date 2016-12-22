#!/bin/sh

ACTION=$1
ITERATIONS=$2

if [ "$ACTION" == "train" ]; then
	# initiate training session
	if [ "$#" -ne "2" ]; then
		ITERATIONS=10
	elif [ "$ITERATIONS" == "inf" ]; then
		while [ 1 -eq 1 ]; 
		do
			python training.py
		done
	else
		echo "Starting a training session of $ITERATIONS training sessions"
		i=1
		while [ $i -le $ITERATIONS ]; 
		do
			python training.py
			i=$((i+1))
		done
	fi
fi