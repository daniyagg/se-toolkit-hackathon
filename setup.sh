#!/bin/bash

# WaterTracker Setup Script
# This script helps set up the PostgreSQL database

echo "=== WaterTracker Database Setup ==="
echo ""

# Check if psql is available
if ! command -v psql &> /dev/null; then
    echo "Error: psql is not installed or not in PATH"
    echo "Please install PostgreSQL first"
    exit 1
fi

echo "Setting up PostgreSQL database..."
echo ""

# Run the schema SQL
psql -U postgres -f backend/schema.sql

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Database setup complete!"
    echo ""
    echo "Next steps:"
    echo "1. cd backend && pip install -r requirements.txt"
    echo "2. uvicorn main:app --reload --host 0.0.0.0 --port 8000"
    echo "3. cd flutter_app && flutter pub get && flutter run"
else
    echo ""
    echo "✗ Database setup failed"
    echo "Please check the error messages above"
    exit 1
fi
