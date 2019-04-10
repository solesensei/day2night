#!/bin/bash

PORT=1434
PSW=""
if [ $# -gt 0 ]; then
	if [ $1 == "stop" ]; then
		echo "Stopping Jupyter Server..."
		jupyter notebook stop $PORT
		echo "Server closed!"
		exit 0
	fi
	PSW="$1"
fi

echo "Starting Jupyter Server on port $PORT..."

jupyter notebook --no-browser --NotebookApp.allow_origin='*' --port=$PORT  --NotebookApp.token=$PSW --NotebookApp.password='' --NotebookApp.disable_check_xsrf=True --allow-root --NotebookApp.ip='0.0.0.0' &

sleep 2

echo "Server started!"
