#!/bin/bash
echo 1 > /sys/class/fpga-bridge/hps2fpga/enable
echo 1 > /sys/class/fpga-bridge/lwhps2fpga/enable 
echo 1 > /sys/class/fpga-bridge/fpga2hps/enable

