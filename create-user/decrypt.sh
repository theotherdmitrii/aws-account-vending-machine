#!/usr/bin/env bash

password=$(echo "${1}" | base64 --decode | gpg -d)

echo user password is ${password}