(() => {
  'use strict';
  const slideHeader = document.querySelector('.top-navbar');
  if (slideHeader && document.querySelector('.slide-page')) {
    const updateSlideOffset = () => {
      document.querySelectorAll('.slide-page').forEach(section => {
        section.style.scrollMarginTop = `${slideHeader.getBoundingClientRect().height + 16}px`;
      });
    };
    new ResizeObserver(updateSlideOffset).observe(slideHeader);
    updateSlideOffset();
  }
  // Slide pages share the same accessible viewer, without changing the site's access gate.
  if (typeof window.openLightbox !== 'function') {
    const dialog = document.createElement('dialog');
    dialog.style.cssText = 'width:min(1100px,94vw);max-height:94vh;padding:16px;border:0;border-radius:6px';
    const close = document.createElement('button');
    close.type = 'button'; close.textContent = 'ปิดภาพ';
    const img = document.createElement('img');
    img.style.cssText = 'display:block;max-width:100%;max-height:72vh;object-fit:contain;margin:12px auto';
    const caption = document.createElement('p');
    close.addEventListener('click', () => dialog.close());
    dialog.append(close, img, caption); document.body.append(dialog);
    window.openLightbox = (src, text) => {
      img.src = src; img.alt = text; caption.textContent = text; dialog.showModal();
    };
  }
  document.querySelectorAll('.reviewed-photo img').forEach(img => {
    img.addEventListener('error', () => {
      const note = document.createElement('p');
      note.className = 'evidence-empty';
      note.textContent = 'ไม่สามารถโหลดภาพหลักฐานนี้ได้';
      img.parentElement.replaceWith(note);
    }, { once: true });
  });
})();
