#!/bin/bash

echo "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install openai jinja2 fastapi uvicorn python-frontmatter markdown requests

echo "Creating folder structure..."
mkdir -p backend/posts generators output static


echo "Creating template files..."
touch agent.py generators/parser.py generators/section_builder.py generators/html_writer.py backend/app.py README.md .env

echo "Setup complete. Next step: Add OpenAI key to .env file"

