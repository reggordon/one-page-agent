from generators.section_selector import select_sections
from generators.html_composer import compose_html

prompt = input("Describe your site: ")
sections = select_sections(prompt)
compose_html(sections)
print("✅ Site generated at output/index.html")
