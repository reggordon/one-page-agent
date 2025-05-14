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


Day 4

/ai-website-builder/
├── app.py
├── templates/
│   └── index.html
├── static/
│   └── css/
│       └── styles.css
├── devtools/
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── Makefile
│   ├── README.md


## 🏁 Running the Project

./venv/bin/python app.py