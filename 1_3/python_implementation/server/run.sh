#!/bin/bash
docker run -it --rm --network-alias z14_network --network z14_network --name z14_server_13_py --ip 172.21.14.4 z14_server_13_py "$@"