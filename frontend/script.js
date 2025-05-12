async function generateSite() {
  const prompt = document.getElementById('promptInput').value;

  const response = await fetch("http://localhost:5050/generate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ prompt })
  });

  const data = await response.json();
  document.getElementById('previewFrame').srcdoc = data.html;
}
