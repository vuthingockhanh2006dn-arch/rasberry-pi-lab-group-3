#!/bin/bash

sleep 10

EMAIL="nguyenthienphat210207@gmail.com"

NAME=$(hostname)
IP=$(hostname -I | awk '{print $1}')

echo "Subject: Raspberry Pi Online

Tên máy: $NAME
IP: $IP" | msmtp "$EMAIL"
