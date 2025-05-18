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
  const viewModeSelect = document.getElementById('viewMode');
  const siteName = getSiteName();

  document.title = `Builder: ${siteName}`;
  document.getElementById('site-name').textContent = `Site: ${siteName}`;

  document.getElementById('openSiteBtn').addEventListener('click', () => {
    const name = document.getElementById('newSiteInput').value.trim();
    if (name) window.open(`/?site=${encodeURIComponent(name)}`, '_blank');
  });

  let currentFramework = "";
  let saveTimeout;
  let defaultCss = '';

  const frameworkLinks = {
    bootstrap: "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css",
    tailwind: "https://cdn.jsdelivr.net/npm/tailwindcss@3.4.1/dist/tailwind.min.css",
    simple: "https://cdn.jsdelivr.net/npm/simpledotcss@1.0.0/simple.min.css"
  };

  fetch('/static/styles.css')
    .then(res => res.text())
    .then(css => { defaultCss = css; });

  // Setup live preview CSS injector
  const styleTag = document.createElement('style');
  styleTag.id = 'live-style-preview';
  document.head.appendChild(styleTag);

  cssTextarea.addEventListener('input', () => {
    if (document.getElementById('liveCssToggle').checked) {
      styleTag.innerHTML = cssTextarea.value;
    }
  });

  viewModeSelect.addEventListener('change', () => {
    const mode = viewModeSelect.value;
    document.body.classList.remove('view-editor', 'view-preview', 'view-mobile', 'view-split');
    document.body.classList.add(`view-${mode}`);
  });

  document.getElementById('cssFramework').addEventListener('change', (e) => {
    const selected = e.target.value;
    const oldLink = document.getElementById('framework-style');
    if (oldLink) oldLink.remove();

    if (frameworkLinks[selected]) {
      const link = document.createElement('link');
      link.id = 'framework-style';
      link.rel = 'stylesheet';
      link.href = frameworkLinks[selected];
      document.head.appendChild(link);
      currentFramework = selected;
    } else {
      currentFramework = '';
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
        config: { endpoints: { byFile: '/uploadFile' }, captionPlaceholder: 'Image caption' }
      },
      delimiter: { class: Delimiter },
      quote: {
        class: Quote,
        inlineToolbar: true,
        config: {
          quotePlaceholder: 'Enter a quote',
          captionPlaceholder: 'Quote author'
        }
      }
    },
    placeholder: 'Start typing your website content here...',
    autofocus: true,

    onReady: () => {
      fetch(`/load?site=${getSiteName()}`)
        .then(res => res.json())
        .then(data => {
          if (data.blocks) editor.render({ blocks: data.blocks });
          if (data.css) cssTextarea.value = data.css;

          // Apply framework
          if (data.framework) {
            document.getElementById('cssFramework').value = data.framework;
            const selected = data.framework;
            const oldLink = document.getElementById('framework-style');
            if (oldLink) oldLink.remove();

            if (frameworkLinks[selected]) {
              const link = document.createElement('link');
              link.id = 'framework-style';
              link.rel = 'stylesheet';
              link.href = frameworkLinks[selected];
              document.head.appendChild(link);
              currentFramework = selected;
            }
          }

          document.body.classList.add('view-split');
        });
    },

    onChange: () => {
      clearTimeout(saveTimeout);
      saveTimeout = setTimeout(() => {
        editor.save().then((outputData) => {
          fetch(`/save?site=${getSiteName()}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              blocks: outputData.blocks,
              css: cssTextarea.value,
              framework: currentFramework
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
    previewContainer.innerHTML = '<div class="site-preview-root" id="previewRoot"></div>';
    const previewRoot = document.getElementById('previewRoot');

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
      previewRoot.appendChild(wrapper);
    });
  }

  document.getElementById('clearCanvas').addEventListener('click', () => {
    const clearedData = {
      blocks: [{ type: 'paragraph', data: { text: '' } }],
      css: ''
    };

    editor.render(clearedData).then(() => {
      previewContainer.innerHTML = '';
      cssTextarea.value = '';

      fetch(`/save?site=${getSiteName()}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(clearedData)
      }).then(() => {
        saveStatus.textContent = 'Canvas cleared';
        setTimeout(() => { saveStatus.textContent = ''; }, 2000);
      });
    });
  });

  document.getElementById('resetCss').addEventListener('click', () => {
    cssTextarea.value = defaultCss;
    if (document.getElementById('liveCssToggle').checked) {
      document.getElementById('live-style-preview').innerHTML = defaultCss;
    }
  });

  document.getElementById('downloadSite').addEventListener('click', () => {
    const link = document.createElement('a');
    link.href = '/downloadZip';
    link.download = 'website.zip';
    link.click();
  });

  function getSiteName() {
    const params = new URLSearchParams(window.location.search);
    return params.get('site') || 'default';
  }
});
