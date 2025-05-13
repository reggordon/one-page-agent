def infer_layout(prompt: str) -> str:
    if "grid" in prompt:
        return "grid-3"
    elif "hero" in prompt:
        return "hero"
    elif "columns" in prompt and "2" in prompt:
        return "grid-2"
    return "default"

def get_layout_template(layout_type: str) -> str:
    if layout_type == "hero":
        return '<section class="py-16 text-center"><h1 class="text-4xl font-bold">[HEADER]</h1><p class="mt-4">[SUBTEXT]</p><a class="mt-6 inline-block bg-blue-500 text-white px-6 py-2 rounded" href="#">Call to Action</a></section>'
    elif layout_type == "grid-3":
        return '<section class="grid grid-cols-1 md:grid-cols-3 gap-6 p-6">[CARDS]</section>'
    return '<section class="p-6">[CONTENT]</section>'
