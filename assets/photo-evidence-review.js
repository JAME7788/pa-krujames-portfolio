(() => {
  'use strict';
  // Keep linked documents and reviewed photographs together in the existing viewer.
  const originalOpen = window.openAlbumModal;
  if (typeof originalOpen !== 'function' || typeof ALBUMS_DATA === 'undefined') return;
  window.openAlbumModal = function (albumId) {
    const album = ALBUMS_DATA.find(item => item.id === albumId);
    if (!album) return;
    originalOpen(albumId);
    const grid = document.getElementById('album-modal-grid');
    const gp = document.querySelector('.album-modal-gp-btn');
    if (gp) gp.hidden = true;
    document.getElementById('album-modal-count').textContent = `${album.items.length} ภาพ · รอบประเมิน 2569`;
    const oldLinks = document.getElementById('album-evidence-links');
    if (oldLinks) oldLinks.remove();
    const links = document.createElement('div');
    links.id = 'album-evidence-links';
    links.className = 'album-evidence-links';
    for (const item of album.links || []) {
      const link = document.createElement('a');
      link.href = item.href;
      link.textContent = item.title;
      if (item.href.startsWith('#')) link.addEventListener('click', () => window.closeAlbumModal());
      else { link.target = '_blank'; link.rel = 'noopener'; }
      links.append(link);
    }
    for (const id of album.related || []) {
      const target = ALBUMS_DATA.find(a => a.id === id);
      if (!target) continue;
      const button = document.createElement('button');
      button.type = 'button';
      button.textContent = target.title;
      button.addEventListener('click', () => window.openAlbumModal(id));
      links.append(button);
    }
    grid.before(links);
    grid.replaceChildren();
    for (const item of album.items) {
      const card = document.createElement('button');
      card.type = 'button';
      card.className = 'album-photo-card';
      const box = document.createElement('div');
      box.className = 'album-photo-thumb-box';
      const img = document.createElement('img');
      img.className = 'album-photo-thumb';
      img.src = item.src; img.alt = item.caption; img.loading = 'lazy';
      box.append(img);
      const info = document.createElement('div'); info.className = 'album-photo-info';
      const kind = document.createElement('span'); kind.className = 'album-photo-kind';
      kind.textContent = item.evidence_kind === 'document' ? 'เอกสาร / สื่อประชาสัมพันธ์' : 'ภาพกิจกรรม';
      const caption = document.createElement('div'); caption.className = 'album-photo-caption'; caption.textContent = item.caption;
      const date = document.createElement('div'); date.className = 'album-photo-date'; date.textContent = item.date;
      info.append(kind, caption, date); card.append(box, info);
      card.addEventListener('click', () => window.openLightbox(item.src, `${item.caption} · ${item.date}`));
      grid.append(card);
    }
    if (!album.items.length) {
      const note = document.createElement('p'); note.className = 'album-document-note';
      note.textContent = 'ดูเอกสารและข้อมูลอ้างอิงจากลิงก์ด้านบน';
      grid.append(note);
    }
  };
})();
