document.addEventListener("DOMContentLoaded", () => {
  const Header = window.Header;
  const Paragraph = window.Paragraph;
  const List = window.List || window.EditorJSList;
  const ImageTool = window.ImageTool;
  const Delimiter = window.Delimiter;
  const Quote = window.Quote;

  const editorContainer = document.getElementById('editor');
  const previewContainer = document.getElementById('preview');
  const cssTextarea = document.getElementById('customCss');
  const saveStatus = document.getElementById('save-status');
  let saveTimeout;

  let defaultCss = '';

fetch('/static/styles.css')
  .then(res => res.text())
  .then(css => {
    defaultCss = css;
  });


  cssTextarea.addEventListener('input', () => {
  const styleTag = document.getElementById('live-style-preview');
  if (styleTag) {
    styleTag.innerHTML = cssTextarea.value;
  }
});




  const editor = new EditorJS({
    holder: 'editor',
    tools: {
      header: { class: Header, inlineToolbar: true },
      paragraph: { class: Paragraph, inlineToolbar: true },
      list: { class: List, inlineToolbar: true },
      image: {
        class: ImageTool,
        config: {
          endpoints: {
            byFile: '/uploadFile'
          },
          captionPlaceholder: 'Image caption',
        }
      },
      delimiter: { class: Delimiter },
      quote: {
        class: Quote,
        inlineToolbar: true,
        config: {
          quotePlaceholder: 'Enter a quote',
          captionPlaceholder: 'Quote author',
        }
      }
    },
    placeholder: 'Start typing your website content here...',
    autofocus: true,
    onReady: () => {
      fetch('/load')
        .then(res => res.json())
        .then(data => {
          if (data.blocks) editor.render({ blocks: data.blocks });
          if (data.css) cssTextarea.value = data.css;
        });
    },
    onChange: () => {
      clearTimeout(saveTimeout);
      saveTimeout = setTimeout(() => {
        editor.save().then((outputData) => {
          const css = cssTextarea.value;

          fetch('/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              blocks: outputData.blocks,
              css: css
            })
          })
          .then(res => res.json())
          .then(() => {
            saveStatus.textContent = `Saved ✓ at ${new Date().toLocaleTimeString()}`;
            setTimeout(() => { saveStatus.textContent = ''; }, 2000);
          });

          renderOutput(outputData);
        });
      }, 1000);
    }
  });

  function renderOutput(data) {
    previewContainer.innerHTML = '';
    data.blocks.forEach(block => {
      const wrapper = document.createElement('div');
      let contentEl;

      switch (block.type) {
        case 'header':
          contentEl = document.createElement('h' + block.data.level);
          contentEl.textContent = block.data.text;
          break;
        case 'paragraph':
          contentEl = document.createElement('p');
          contentEl.textContent = block.data.text;
          break;
        case 'list':
          contentEl = document.createElement(block.data.style === 'ordered' ? 'ol' : 'ul');
          block.data.items.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            contentEl.appendChild(li);
          });
          break;
        case 'delimiter':
          contentEl = document.createElement('hr');
          break;
        case 'quote':
          contentEl = document.createElement('blockquote');
          contentEl.innerHTML = `<p>"${block.data.text}"</p><footer>— ${block.data.caption}</footer>`;
          break;
        case 'image':
          contentEl = document.createElement('div');
          contentEl.innerHTML = `
            <img src="${block.data.file.url}" alt="${block.data.caption || ''}" style="max-width: 100%; border-radius: 0.5rem;">
            ${block.data.caption ? `<p style="text-align: center;">${block.data.caption}</p>` : ''}
          `;
          break;
        default:
          contentEl = document.createElement('div');
          contentEl.textContent = `[Unsupported block: ${block.type}]`;
      }

      wrapper.appendChild(contentEl);
      previewContainer.appendChild(wrapper);
    });
  }

  
  document.getElementById('clearCanvas').addEventListener('click', () => {
  const clearedData = {
    blocks: [
      {
        type: 'paragraph',
        data: { text: '' }
      }
    ],
    css: ''
  };

  editor.render(clearedData).then(() => {
    previewContainer.innerHTML = '';
    const cssTextarea = document.getElementById('customCss');
    if (cssTextarea) cssTextarea.value = '';

    fetch('/save', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(clearedData)
    }).then(() => {
      saveStatus.textContent = 'Canvas cleared';
      setTimeout(() => { saveStatus.textContent = ''; }, 2000);
    });
  }).catch(err => {
    console.error("Error clearing canvas:", err);
  });
});

document.getElementById('resetCss').addEventListener('click', () => {
  cssTextarea.value = defaultCss;

  if (document.getElementById('liveCssToggle').checked) {
    document.getElementById('live-style-preview').innerHTML = defaultCss;
  }
});




  // Download full site zip
  document.getElementById('downloadSite').addEventListener('click', () => {
    const link = document.createElement('a');
    link.href = '/downloadZip';
    link.download = 'website.zip';
    link.click();
  });
});
