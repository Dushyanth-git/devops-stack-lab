# ScoreRecords DevOps Platform

A production-style, containerized full-stack sample app that demonstrates how to ship a simple records system using **FastAPI + Streamlit**, automate delivery with **Jenkins**, and prepare observability with **Grafana/Loki/Promtail**.

## Why this repository exists

This project is designed as a practical DevOps learning sandbox where you can:
- Build and package backend/frontend services with Docker.
- Push versioned images to Docker Hub from a CI pipeline.
- Deploy tagged releases to a remote host via Docker Compose.
- Extend the stack with centralized logging and dashboards.

## Project architecture

- **Backend** (`app/backend`): FastAPI service that stores score records in an Excel file.
- **Frontend** (`app/frontend`): Streamlit UI for adding and viewing records.
- **CI/CD** (`Jenkinsfile`): Builds images in one Ec2, pushes to Docker Hub, then deploys to another EC2 over SSH.
- **Runtime deployment** (`infra/docker/docker-compose.yml`): Pulls and runs tagged backend/frontend images.
- **Observability** (`observability/logs-compose.yml`): Loki + Promtail + Grafana stack.

## Core features

- Add and list score records through a simple web UI.
- Persistent storage using `data.xlsx` in the backend container context.
- Image tagging by Git commit SHA for traceable deployments.
- Lightweight observability stack ready for log aggregation.

## Quick start (local)

> This repo currently includes deployment compose files for image-based runtime. For local development, build and run each service container from `app/backend` and `app/frontend`.

Backend:
```bash
cd app/backend
docker build -t local-backend .
docker run --rm -p 8000:8000 local-backend
```

Frontend (new terminal):
```bash
cd app/frontend
docker build -t local-frontend .
docker run --rm -p 8501:8501 --add-host=backend:host-gateway local-frontend
```

Then open `http://localhost:8501`.

## CI/CD flow summary

1. Jenkins checks out code and derives short commit SHA.
2. Builds backend/frontend images.
3. Pushes both images to Docker Hub.
4. SSHes into deployment host, sets `IMAGE_TAG`, and runs `docker compose pull && docker compose up -d`.

## Tech stack

- Python, FastAPI, Uvicorn
- Streamlit
- Docker, Docker Compose
- Jenkins
- Grafana, Loki, Promtail
