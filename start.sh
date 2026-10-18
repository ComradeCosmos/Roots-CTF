#!/usr/bin/env bash
echo "==================================================="
echo "  RootsCTF / Civilization - CTFd Server Launcher"
echo "==================================================="
echo ""
cd CTFd
if [ -f "../.venv/bin/python" ]; then
    ../.venv/bin/python serve.py --port 8000
elif [ -f ".venv/bin/python" ]; then
    .venv/bin/python serve.py --port 8000
else
    python3 serve.py --port 8000
fi
