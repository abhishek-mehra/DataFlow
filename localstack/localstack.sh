#!/bin/bash
# This script will be executed when LocalStack starts
awslocal sqs create-queue --queue-name dataflow-queue
