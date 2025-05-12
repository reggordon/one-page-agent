onepager-agent/
├── templates/
│   ├── hero.html
│   ├── about.html
│   ├── contact.html
│   └── base.html
├── generators/
│   ├── section_selector.py
│   └── html_composer.py
├── output/
│   └── index.html
├── static/
│   └── tailwind.min.css
├── agent.py
├── requirements.txt
├── Dockerfile
└── .env  (optional, not used yet)


## 🏁 Restarting the Project

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
