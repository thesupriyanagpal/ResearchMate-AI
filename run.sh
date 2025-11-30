#!/bin/bash

# Start Backend
echo "Starting Backend..."
cd backend
# Check if venv exists, if not create it (optional, assuming user has set it up)
# python3 -m venv venv
# source venv/bin/activate
# pip install -r requirements.txt
python3 -m uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!

# Start Frontend
echo "Starting Frontend..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

# Handle shutdown
trap "kill $BACKEND_PID $FRONTEND_PID" EXIT

wait
