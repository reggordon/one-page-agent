from jinja2 import Environment, FileSystemLoader

def compose_html(parsed):
    env = Environment(loader=FileSystemLoader("templates"))
    base = env.get_template("base.html")

    content = ""
    for name in parsed["sections"]:
        section = env.get_template(f"{name}.html")
        content += section.render(include_image=parsed["include_image"])

    output = base.render(content=content)

    with open("output/index.html", "w") as f:
        f.write(output)
