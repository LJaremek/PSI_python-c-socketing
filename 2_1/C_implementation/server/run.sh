#!/bin/bash
docker run -it --rm --network-alias z14_network --network z14_network --name z14_server_21_c --ip 172.21.14.3 z14_server_21_c "$@"