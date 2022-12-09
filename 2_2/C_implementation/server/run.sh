#!/bin/bash
docker run -it --rm --network-alias z14_network --network z14_network --name z14_server_22_c --ip 172.21.14.5 z14_server_22_c "$@"