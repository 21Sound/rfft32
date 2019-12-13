cmake_minimum_required(VERSION 2.8)

project(rfft32)

set(LIB_NAME "rfft32")

set(RFFT32LIB_SOURCES
        "rfft32.h"
        "rfft32.c"
        )

set(EXEC_NAME "rfft32Bin")

set(RFFT32BIN_SOURCES
	"main.c"
	)

add_library(${LIB_NAME} SHARED ${RFFT32LIB_SOURCES})

add_executable(${EXEC_NAME} ${RFFT32BIN_SOURCES})

target_link_libraries(${EXEC_NAME} ${LIB_NAME})
