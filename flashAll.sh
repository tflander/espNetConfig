#!/usr/bin/env bash

ampy --port /dev/cu.SLAB_USBtoUART put boot.py
ampy --port /dev/cu.SLAB_USBtoUART put configHttpServer.py
ampy --port /dev/cu.SLAB_USBtoUART put netConfig.py
ampy --port /dev/cu.SLAB_USBtoUART put simpleHttpServer.py
ampy --port /dev/cu.SLAB_USBtoUART put config.py
ampy --port /dev/cu.SLAB_USBtoUART put main.py
ampy --port /dev/cu.SLAB_USBtoUART put networkStatusNotifier.py

ampy --port /dev/cu.SLAB_USBtoUART ls
