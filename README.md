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


project-root/
├── app.py                  ✅ Flask app for local web preview
├── backend/
│   ├── main.py             ✅ Orchestrates prompt → layout → style
│   ├── layout_engine.py    ✅ Handles structural logic
│   └── style_engine.py     ✅ Applies Tailwind classes
├── templates/
│   └── base.html           ✅ Optional Jinja wrapper
├── static/
│   └── style.css
├── data/
│   └── output.html         ✅ Final generated file


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


Day three

| generate-page | creates page|
| serve-frontend | launches server|
| preview-page | shows page on http://localhost:3000/output.html |


# Build the Docker image

docker compose -f docker-compose.daythree.yml up --build

# kill the container
docker compose -f docker-compose.daythree.yml down


View on  : http://localhost:3000/output.html
