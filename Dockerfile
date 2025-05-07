# Use slim Python base
FROM python:3.10-slim

# Create working dir
WORKDIR /app

# Copy project files
COPY . .

# Install pip and deps
RUN pip install --upgrade pip && pip install -r requirements.txt

# Create output directory at build time
RUN mkdir -p output

# Default run: launch the agent
CMD ["python", "agent.py"]
