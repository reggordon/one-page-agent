from bs4 import BeautifulSoup

def apply_tailwind_styles(raw_html: str) -> str:
    soup = BeautifulSoup(raw_html, "html.parser")

    def add_classes(tag, class_list):
        existing = tag.get('class', [])
        if isinstance(existing, str):
            existing = existing.split()
        tag['class'] = existing + class_list

    for tag in soup.find_all("h1"):
        add_classes(tag, ['text-4xl', 'font-bold'])
    
    for tag in soup.find_all("p"):
        add_classes(tag, ['text-base', 'text-gray-600'])

    for tag in soup.find_all("a"):
        add_classes(tag, ['text-blue-500', 'underline'])

    for tag in soup.find_all("section"):
        add_classes(tag, ['py-8', 'px-4'])

    return str(soup)
