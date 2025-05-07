def select_sections(prompt):
    prompt = prompt.lower()
    options = ["hero", "about", "services", "contact"]
    return [sec for sec in options if sec in prompt]
