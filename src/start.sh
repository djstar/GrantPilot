#!/bin/bash
set -e

# GrantPilot Startup Script
# This script starts all services using Docker Compose

echo "🚀 Starting GrantPilot..."

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check for Docker Compose
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Navigate to script directory
cd "$(dirname "$0")"

# Create data directories if they don't exist
mkdir -p data/postgresql data/redis data/uploads data/backups

# Build and start services
echo "📦 Building containers..."
docker compose build

echo "🐘 Starting PostgreSQL and Redis..."
docker compose up -d db redis

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
until docker compose exec -T db pg_isready -U grantpilot 2>/dev/null; do
    sleep 1
done
echo "✅ PostgreSQL is ready"

# Start backend
echo "🐍 Starting FastAPI backend..."
docker compose up -d backend

# Wait for backend to be ready
echo "⏳ Waiting for backend to be ready..."
until curl -s http://localhost:8000/api/v1/health > /dev/null 2>&1; do
    sleep 1
done
echo "✅ Backend is ready"

# Start frontend
echo "⚛️  Starting React frontend..."
docker compose up -d frontend

echo ""
echo "✨ GrantPilot is running!"
echo ""
echo "📍 Frontend: http://localhost:5173"
echo "📍 Backend API: http://localhost:8000/api/v1"
echo "📍 API Docs: http://localhost:8000/docs"
echo ""
echo "To view logs: docker compose logs -f"
echo "To stop: docker compose down"
