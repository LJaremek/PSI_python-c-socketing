#!/bin/bash
docker run -it --rm --network-alias z14_network --network z14_network --name z14_server_25_py --ip 172.21.14.6 z14_server_25_py "$@"
