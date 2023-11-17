#!/bin/bash

# Stop Docker Compose services
docker-compose down

# Remove all unused volumes
docker volume prune -f

# Remove all unused containers, networks, and images (both dangling and unreferenced)
docker system prune -af

echo "Docker cleanup complete."

git pull

docker compose up -d
