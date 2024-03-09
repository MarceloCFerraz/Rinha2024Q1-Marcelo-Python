#!/usr/bin/env bash

# build the image
docker build -t rinha2024q1-marcelo-python --platform linux/amd64 --build-arg TARGET_RUNTIME=linux-x64 .

# update tag 'latest'
docker tag rinha2024q1-marcelo-python marcelocferraz/rinha2024q1-marcelo-python:latest

# push changes to docker hub
docker push marcelocferraz/rinha2024q1-marcelo-python:latest
