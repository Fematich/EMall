#!/bin/bash

sudo mkdir /tmp/ramdisk; chmod 777 /tmp/ramdisk
sudo mount -t tmpfs -o size=13G tmpfs /tmp/ramdisk/

sudo cp -r /work/index /tmp/ramdisk/index

sudo logsave /proj/CMSearch/logs/termlist.log python termlistgen.py

sudo cp /work/termlist /users/Mfeys
