/* =====================================================================
   Furner RefraCeram — main.js
   Vanilla JS, no dependencies. Drives nav state, mobile menu,
   scroll reveals, hero sparks, and small ergonomic details.
   ===================================================================== */

(function () {
  'use strict';

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ----- Nav: shadow + blur on scroll -----
  const nav = document.querySelector('[data-nav]');
  if (nav) {
    const onScroll = () => {
      if (window.scrollY > 40) nav.classList.add('is-scrolled');
      else nav.classList.remove('is-scrolled');
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  // ----- Mobile menu -----
  const burger = document.querySelector('[data-burger]');
  const mobileMenu = document.querySelector('[data-mobile-menu]');
  let lastFocused = null;

  function openMobileMenu() {
    if (!mobileMenu || !burger) return;
    lastFocused = document.activeElement;
    mobileMenu.classList.add('is-open');
    burger.classList.add('is-open');
    burger.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
    const firstLink = mobileMenu.querySelector('a, button');
    if (firstLink) firstLink.focus();
  }

  function closeMobileMenu() {
    if (!mobileMenu || !burger) return;
    mobileMenu.classList.remove('is-open');
    burger.classList.remove('is-open');
    burger.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
    if (lastFocused && typeof lastFocused.focus === 'function') lastFocused.focus();
  }

  if (burger && mobileMenu) {
    burger.addEventListener('click', () => {
      if (mobileMenu.classList.contains('is-open')) closeMobileMenu();
      else openMobileMenu();
    });
    mobileMenu.querySelectorAll('a').forEach((a) => {
      a.addEventListener('click', closeMobileMenu);
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && mobileMenu.classList.contains('is-open')) closeMobileMenu();
    });
    // Focus trap
    mobileMenu.addEventListener('keydown', (e) => {
      if (e.key !== 'Tab') return;
      const focusable = mobileMenu.querySelectorAll('a, button, [tabindex]:not([tabindex="-1"])');
      if (!focusable.length) return;
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    });
  }

  // ----- Dropdown (desktop click toggle) -----
  document.querySelectorAll('[data-dropdown]').forEach((dd) => {
    const toggle = dd.querySelector('[data-dropdown-toggle]');
    if (!toggle) return;
    toggle.addEventListener('click', (e) => {
      e.preventDefault();
      const isOpen = dd.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
    document.addEventListener('click', (e) => {
      if (!dd.contains(e.target)) {
        dd.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  });

  // ----- Scroll reveals via IntersectionObserver -----
  if ('IntersectionObserver' in window) {
    const targets = document.querySelectorAll('[data-reveal]');
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-revealed');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -50px 0px' });
    targets.forEach((t) => io.observe(t));
  } else {
    document.querySelectorAll('[data-reveal]').forEach((t) => t.classList.add('is-revealed'));
  }

  // ----- Spark animation on every dark layer -----
  if (!prefersReducedMotion) {
    document.querySelectorAll('[data-sparks]').forEach((sparkLayer) => {
      const h = sparkLayer.offsetHeight || 480;
      const maxLive = Math.max(4, Math.min(18, Math.round(h / 40)));
      const interval = Math.max(180, Math.round(5000 / maxLive));
      const initialBurst = Math.min(maxLive, Math.max(3, Math.round(maxLive * 0.6)));
      const spawnSpark = () => {
        const spark = document.createElement('div');
        spark.className = 'spark';
        const w = sparkLayer.offsetWidth;
        const x = Math.random() * w;
        const dx = (Math.random() - 0.5) * 80;
        const duration = 3 + Math.random() * 2;
        const size = 2 + Math.random() * 3;
        spark.style.left = x + 'px';
        spark.style.width = size + 'px';
        spark.style.height = size + 'px';
        spark.style.setProperty('--dx', dx + 'px');
        spark.style.animationDuration = duration + 's';
        spark.style.opacity = 0.7 + Math.random() * 0.3;
        sparkLayer.appendChild(spark);
        setTimeout(() => spark.remove(), duration * 1000 + 200);
      };
      for (let i = 0; i < initialBurst; i++) {
        setTimeout(spawnSpark, i * 240);
      }
      setInterval(() => {
        if (sparkLayer.querySelectorAll('.spark').length < maxLive) spawnSpark();
      }, interval);
    });
  }

  // ----- Footer year -----
  document.querySelectorAll('[data-year]').forEach((el) => {
    el.textContent = new Date().getFullYear();
  });

  // ----- Smooth-scroll for in-page anchors with fixed-nav offset -----
  document.querySelectorAll('a[href^="#"]:not([href="#"])').forEach((link) => {
    link.addEventListener('click', (e) => {
      const id = link.getAttribute('href').slice(1);
      const target = document.getElementById(id);
      if (!target) return;
      e.preventDefault();
      const navHeight = nav ? nav.offsetHeight : 0;
      const y = target.getBoundingClientRect().top + window.pageYOffset - navHeight - 16;
      window.scrollTo({ top: y, behavior: prefersReducedMotion ? 'auto' : 'smooth' });
    });
  });

  // ----- Mark current page in nav -----
  const here = (location.pathname.split('/').pop() || 'index.html').toLowerCase();
  document.querySelectorAll('[data-nav-link]').forEach((link) => {
    const href = (link.getAttribute('href') || '').toLowerCase();
    if (href === here) link.classList.add('is-current');
  });

})();
