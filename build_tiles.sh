#!/bin/bash

echo "Building tiles..." && \
  rm -rf ./output/states/* && \
  rm -rf ./output/counties/* && \
  docker-compose build && \
  docker-compose up
