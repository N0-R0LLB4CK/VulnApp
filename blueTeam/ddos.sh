#!/bin/bash

for i in {1..60}; do curl -s -o /dev/null -w "%{http_code}\n" http://63.176.160.32/; done