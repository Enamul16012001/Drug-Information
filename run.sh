#!/bin/bash
echo "Starting Drug Search Application..."
echo "Access the app at: http://localhost:8000"
echo "Press Ctrl+C to stop"
uvicorn main:app --reload --host 0.0.0.0 --port 8012