from jinja2 import Environment, FileSystemLoader

def compose_html(section_names):
    env = Environment(loader=FileSystemLoader("templates"))
    base = env.get_template("base.html")
    
    content = ""
    for name in section_names:
        section = env.get_template(f"{name}.html")
        content += section.render()

    output = base.render(content=content)

    with open("output/index.html", "w") as f:
        f.write(output)
