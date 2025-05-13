# watch_and_build.py
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time, subprocess

class PromptChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith("prompt.txt"):
            print("🔁 prompt.txt changed, regenerating...")
            subprocess.run(["./venv/bin/python", "-m", "backend.main", open("prompt.txt").read()])

observer = Observer()
observer.schedule(PromptChangeHandler(), path=".", recursive=False)
observer.start()

print("👀 Watching prompt.txt for changes. Press Ctrl+C to stop.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
