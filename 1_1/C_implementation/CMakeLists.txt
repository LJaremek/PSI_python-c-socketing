cmake_minimum_required(VERSION 3.23)
project(python_c_socketing_psi C)

set(CMAKE_C_STANDARD 11)

include_directories(.)

add_executable(c_udp_client
        UDPClient.c
        )

add_executable(c_udp_server
        UDPServer.c
        )
