def select_sections(prompt):
    prompt = prompt.lower()
    sections = []

    if "hero" in prompt:
        sections.append("hero")
    if "about" in prompt:
        sections.append("about")
    if "services" in prompt:
        sections.append("services")
    if "contact" in prompt:
        sections.append("contact")

    return {
        "sections": sections,
        "include_image": any(kw in prompt for kw in ["image", "photo", "hero image", "add image"])
    }
