/* ==========================================================================
   Insights LLC — small amount of JavaScript
   1. The two service cards flip over when you select them.
   2. The footer year keeps itself up to date.
   Nothing here needs editing when you change the words on the site.
   ========================================================================== */
(function () {
  'use strict';

  /* ---------- 1. Flip cards ---------- */
  var cards = Array.prototype.slice.call(document.querySelectorAll('[data-card]'));
  var sideBySide = window.matchMedia('(min-width: 861px)');
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  var entries = cards.map(function (card) {
    return {
      card: card,
      front: card.querySelector('.card__face--front'),
      back: card.querySelector('.card__face--back')
    };
  }).filter(function (e) { return e.front && e.back; });

  // A card is as tall as the side that is showing. When the cards sit
  // beside each other, un-flipped cards share the tallest front height so
  // their bottom edges line up.
  var measuring = false;
  function setHeights() {
    if (measuring || !entries.length) return;
    measuring = true;

    // Measure both sides at their natural height.
    entries.forEach(function (e) { e.front.style.minHeight = ''; });
    var fronts = entries.map(function (e) { return e.front.offsetHeight; });
    var backs  = entries.map(function (e) { return e.back.offsetHeight; });
    var tallestFront = sideBySide.matches ? Math.max.apply(null, fronts) : 0;

    entries.forEach(function (e, i) {
      var flipped = e.card.classList.contains('is-flipped');
      var height = flipped ? backs[i] : Math.max(fronts[i], tallestFront);
      e.card.style.height = height + 'px';
      // Stretch the visible front so both cards end on the same line.
      e.front.style.minHeight = flipped ? '' : height + 'px';
    });

    measuring = false;
  }

  // Hide the side facing away from screen readers and the tab order.
  function setFaceState(e) {
    var flipped = e.card.classList.contains('is-flipped');
    [[e.front, flipped], [e.back, !flipped]].forEach(function (pair) {
      var el = pair[0], hidden = pair[1];
      el.setAttribute('aria-hidden', hidden ? 'true' : 'false');
      if (hidden) { el.setAttribute('inert', ''); } else { el.removeAttribute('inert'); }
    });
    var trigger = e.front.querySelector('[data-flip]');
    if (trigger) trigger.setAttribute('aria-expanded', flipped ? 'true' : 'false');
  }

  function flip(e) {
    e.card.classList.toggle('is-flipped');
    setFaceState(e);
    setHeights();

    // Keep the top of the card in view, which matters most on a phone.
    var top = e.card.getBoundingClientRect().top;
    if (top < 70) {
      window.scrollTo({
        top: window.pageYOffset + top - 90,
        behavior: reduceMotion.matches ? 'auto' : 'smooth'
      });
    }
  }

  entries.forEach(function (e) {
    // Selecting anywhere on the front of the card turns it over.
    e.front.addEventListener('click', function (event) {
      if (event.target.closest('a')) return; // let real links do their job
      flip(e);
    });

    // The "Read more" and "Back" buttons.
    Array.prototype.forEach.call(e.card.querySelectorAll('[data-flip]'), function (button) {
      button.addEventListener('click', function (event) {
        event.stopPropagation();
        flip(e);
      });
    });

    setFaceState(e);
  });

  if (entries.length) {
    // Keep the heights right as images load, fonts arrive or the window changes.
    if (window.ResizeObserver) {
      var observer = new ResizeObserver(setHeights);
      entries.forEach(function (e) { observer.observe(e.front); observer.observe(e.back); });
    }
    window.addEventListener('resize', setHeights);
    window.addEventListener('load', setHeights);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(setHeights);
    setHeights();
  }

  /* ---------- 2. Footer year ---------- */
  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
})();
