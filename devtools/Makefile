# === Local Dev Environment (No Docker) ===

setup:
	python3 -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements.txt
	./venv/bin/pip freeze > requirements.txt

run-backend:
	@echo "🚀 Starting Flask backend on http://localhost:5000"
	./venv/bin/python backend/app.py

serve-frontend:
	@echo "🌐 Serving frontend on http://localhost:3000"
	cd frontend && python3 -m http.server 3000

restart: stop
	@make -j2 run-backend serve-frontend

stop:
	@echo "🔻 Killing servers on ports 5050 and 3000 if they exist"
	@lsof -ti :5050 | xargs kill -9 2>/dev/null || true
	@lsof -ti :3000 | xargs kill -9 2>/dev/null || true

clean: stop
	@echo "🧹 Removing virtual environment"
	rm -rf venv

generate-page:
	@echo "🧠 Generating styled HTML using module mode"
	./venv/bin/python -m backend.main "hero section with call to action and three product cards"


test-layout:
	@echo "🔧 Testing layout inference"
	./venv/bin/python -c "from backend.layout_engine import infer_layout; print(infer_layout('3-column grid with testimonials and a call-to-action'))"

generate-from-file:
	@echo "📄 Generating page from prompt.txt"
	./venv/bin/python -m backend.main "$$(cat prompt.txt)"

watch:
	./venv/bin/python watch_and_build.py


