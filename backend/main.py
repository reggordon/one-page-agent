import os
import sys
from backend.layout_engine import infer_layout, get_layout_template
from backend.style_engine import apply_tailwind_styles

def build_page(prompt: str):
    layout_type = infer_layout(prompt)
    layout_html = get_layout_template(layout_type)

    # 🔧 Replace placeholders with prompt-aware content
    final_html = layout_html
    final_html = final_html.replace("[HEADER]", f"{prompt.title()}")
    final_html = final_html.replace("[SUBTEXT]", f"Generated layout for: '{prompt}'")
    final_html = final_html.replace("[CARDS]", "<div class='p-4 bg-white rounded shadow'>Card</div>" * 2)
    final_html = final_html.replace("[CONTENT]", f"<p>{prompt}</p>")

    ...


    styled_html = apply_tailwind_styles(final_html)

    # ✅ Wrap in a complete HTML document
    full_page = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <title>Generated Page</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-50 font-sans">
        {styled_html}
    </body>
    </html>
    """

    # ✅ Ensure output goes to frontend/output.html
    output_dir = "frontend"
    output_file = os.path.join(output_dir, "output.html")

    os.makedirs(output_dir, exist_ok=True)

    with open(output_file, "w") as f:
        f.write(full_page.strip())

    print(f"✅ Wrote styled HTML to {output_file}")

# ✅ CLI support
if __name__ == "__main__":
    prompt = sys.argv[1] if len(sys.argv) > 1 else "hero section with CTA and three feature cards"
    build_page(prompt)
