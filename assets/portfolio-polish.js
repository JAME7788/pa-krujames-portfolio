(() => {
  'use strict';
  const header = document.querySelector('.site-header');
  const navigation = document.querySelector('.pa-stepper-wrapper');
  if (!header || !navigation) return;
  // Keep section links clear of both navigation rows as text wraps.
  const updateOffsets = () => {
    document.documentElement.style.setProperty('--report-header-height', `${header.offsetHeight}px`);
    document.documentElement.style.setProperty('--report-nav-height', `${navigation.offsetHeight}px`);
  };
  const observer = new ResizeObserver(updateOffsets);
  observer.observe(header);
  observer.observe(navigation);
  updateOffsets();
})();
