# Dev Tools Archive

This folder contains optional tooling for Docker, Makefile-based CLI, and `.env` files.

These are not used in the current MVP build but can be reinstated for:

- Cloud deployment
- Local LLM inference
- Team collaboration
- Containerized CI environments

To restore:
1. Move `Dockerfile`, `.dockerignore`, `Makefile`, etc. back to the project root.
2. Adjust commands as needed.



To start everything in Docker:

```bash
cd onepager-agent
docker compose up --build

To clean up Docker

docker compose down


To run a Makefile ( lighter)

| Command               | What It Does                                  |
| --------------------- | --------------------------------------------- |
| `make setup`          | Create venv and install deps                  |
| `make run-backend`    | Run Flask API on port 5000                    |
| `make serve-frontend` | Serve `index.html` on port 3000               |
| `make restart`        | Kills old servers, then restarts backend + UI |
| `make stop`           | Kills anything using ports 5000 or 3000       |
| `make clean`          | Stops servers and deletes venv                |


Day three

| generate-page | creates page|
| serve-frontend | launches server|
| preview-page | shows page on http://localhost:3000/output.html |


# Build the Docker image

docker compose -f docker-compose.daythree.yml up --build

# kill the container
docker compose -f docker-compose.daythree.yml down


View on  : http://localhost:3000/output.html

