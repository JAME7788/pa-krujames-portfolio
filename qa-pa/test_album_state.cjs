const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const source = fs.readFileSync('index.html', 'utf8');
const listeners = {};
function element() {
  const classes = new Set();
  return { style: {}, children: [], classList: {
    add: x => classes.add(x), remove: x => classes.delete(x), contains: x => classes.has(x)
  }, appendChild(x) { this.children.push(x); } };
}
const elements = Object.fromEntries(['album-modal','album-modal-badge','album-modal-title','album-modal-count','album-modal-desc','album-modal-grid','lightbox','lightbox-img','lightbox-caption'].map(x => [x, element()]));
const body = element();
const document = {body, getElementById: id => elements[id], querySelector: () => element(), createElement: element,
  addEventListener: (event,fn) => { listeners[event] = fn; }};
const context = vm.createContext({document, window: { addEventListener() {} }, console});
const albumCode = 'function openAlbumModal(' + source.split('    function openAlbumModal(')[1].split('    // Interactive Before/After')[0];
const lightboxCode = 'function openLightbox(' + source.split('    function openLightbox(')[1].split('    // Mobile Navigation Toggle')[0];
vm.runInContext('const ALBUMS_DATA = '+source.split('const ALBUMS_DATA = ')[1].split('\n')[0]+lightboxCode+albumCode, context);
vm.runInContext("openAlbumModal('album-2-2')", context);
assert(elements['album-modal'].classList.contains('active'));
assert(elements['album-modal-grid'].children.length > 0);
assert.equal(body.style.overflow,'hidden');
vm.runInContext("openLightbox('test.jpg','Test')", context);
assert(elements.lightbox.classList.contains('active'));
let stopped = false;
listeners.keydown({key:'Escape',stopImmediatePropagation(){stopped=true;}});
assert(stopped);
assert(!elements.lightbox.classList.contains('active'));
assert(elements['album-modal'].classList.contains('active'));
assert.equal(body.style.overflow,'hidden');
vm.runInContext('closeAlbumModal()', context);
assert(!elements['album-modal'].classList.contains('active'));
assert.equal(body.style.overflow,'auto');
console.log('PASS album 2.2 open, photo open, Escape closes photo only, album close restores scroll');
