#!/bin/bash

# List all processes using NVIDIA devices
nvidia_processes=$(lsof /dev/nvidia* | awk '{print $2}' | grep -v "PID")

# Check if there are any processes to kill
if [ -z "$nvidia_processes" ]; then
	echo "No NVIDIA processes found."
else
	# Loop through and kill each process
	for pid in $nvidia_processes; do
		echo "Killing process $pid"
		sudo kill -9 $pid
	done

	# Unload NVIDIA kernel modules after processes are killed
	echo "Unloading NVIDIA kernel modules..."
	sudo rmmod nvidia
	sudo rmmod nvidia_modeset
	sudo rmmod nvidia_uvm

	echo "NVIDIA processes stopped and modules unloaded."
fi
