document.querySelectorAll('[data-year]').forEach((node) => {
  node.textContent = new Date().getFullYear();
});

const lifecyclePersonas = {
  '40s': {
    persona: 'Juggling work and family',
    about: 'You keep everyone’s health on track between work, children and an aging parent, with little time to spare.',
    color: '#06b6d4',
    light: '#ecfeff',
    miss: [
      'Portals split labs and messages by provider, missing the daily family health context',
      'Bluetooth devices report raw readings without explaining combined risk shifts',
      'Medication apps remind the individual but fail to coordinate support with a spouse or parent'
    ],
    adds: [
      'Combines personal profile and trends from vitals and labs to analyze risk for the whole house',
      'Uses camera vitals, Bluetooth cuffs, oximeters, and scales to capture a complete healthy baseline',
      'Communicates risk shifts and next steps to the Star and care circle without noisy surveillance'
    ],
    photo: 'assets/home/ages/star-40s.webp',
    photoAlt: 'A man in his mid forties looks at his phone at the family kitchen table in the evening.',
    adoption: ['Quick to set up', 'Your family can follow along', 'Alerts only when something matters']
  },
  '50s': {
    persona: 'At the peak of your career',
    about: 'You are busy at the top of your working life, when early changes in blood pressure, sugar or heart rate are easy to put off.',
    color: '#2f80ed',
    light: '#eff6ff',
    miss: [
      'Vitals apps ignore lab results, medication history, and baseline family context',
      'Bluetooth monitors collect data but fail to explain why a specific risk is changing',
      'Patient portals lack the ability to connect daily routines to clinical trend shifts'
    ],
    adds: [
      'Combines personal profiles with vitals and lab trends to detect cardiometabolic drift early',
      'Syncs wearables, Bluetooth cuffs, oximeters, scales, and camera vitals into one clinical story',
      'Differentiates healthy baseline from risk shifts to communicate next steps to the Star and care circle'
    ],
    photo: 'assets/home/ages/star-50s.webp',
    photoAlt: 'A woman in her mid fifties reads her phone on the living-room sofa.',
    adoption: ['Full detail on your own readings', 'Step-by-step setup, if you want it', 'A report ready to share with your doctor']
  },
  '60s': {
    persona: 'Newly retired',
    about: 'You are leaving work behind, with more appointments, medicines and lab results to keep track of.',
    color: '#6366f1',
    light: '#eef2ff',
    miss: [
      'Task apps manage reminders but ignore vitals, labs, and family visibility',
      'Portals create fragmented data silos instead of one calm operating picture',
      'Safety apps focus on emergency response rather than gradual recovery or decline'
    ],
    adds: [
      'Unified organization for appointments, medications, labs, and baseline drift',
      'Consent-safe visibility for family before a crisis occurs while Star stays in control',
      'Guided UX that reduces technical burden while preserving user independence'
    ],
    photo: 'assets/home/ages/star-60s.webp',
    photoAlt: 'A man in his mid sixties checks his phone on his back porch, a cup of tea beside him.',
    adoption: ['Step-by-step setup', 'Screens that are easy to read', 'Fewer choices; invite family when you are ready']
  },
  '70s': {
    persona: 'Living independently',
    about: 'You live at home on your own terms; your family wants peace of mind without hovering.',
    color: '#f59e0b',
    light: '#fffbeb',
    miss: [
      'Emergency apps react late',
      'Location apps lack health and routine context',
      'Medication apps do not show family what changed'
    ],
    adds: [
      'Medication confidence, recovery support and safety confidence',
      'Trusted alerts with health context',
      'Family peace of mind while the Star keeps control'
    ],
    photo: 'assets/home/ages/star-70s.webp',
    photoAlt: 'A man in his mid seventies, in reading glasses, looks at his phone in his armchair.',
    adoption: ['Simple screens', 'Large buttons and text', 'Your family can help you set it up']
  },
  '80s': {
    persona: 'Supported by family',
    about: 'Your family sets things up and keeps watch, so you have as little to do as possible.',
    color: '#ef4444',
    light: '#fef2f2',
    miss: [
      'Single-purpose apps solve narrow moments',
      'Emergency tools lack broader care context',
      'Family often still has to piece together what happened'
    ],
    adds: [
      'Cognitive backup, location confidence and coordinated care',
      'Fall or help response with broader signal context',
      'Angel view with minimal Star burden'
    ],
    photo: 'assets/home/ages/star-80s.webp',
    photoAlt: 'A woman in her mid eighties smiles at her phone in her armchair, a blanket over her knees.',
    adoption: ['Your family sets it up for you', 'Fall and safe-area alerts work without you doing anything', 'The largest, clearest text']
  }
};

document.querySelectorAll('[data-lifecycle-map]').forEach((map) => {
  const tabs = Array.from(map.querySelectorAll('[data-lifecycle-tab]'));
  const persona = map.querySelector('[data-lifecycle-persona]');
  const about = map.querySelector('[data-lifecycle-about]');
  const miss = map.querySelector('[data-lifecycle-miss]');
  const adds = map.querySelector('[data-lifecycle-adds]');
  const adoption = map.querySelector('[data-lifecycle-adoption]');
  const photo = map.querySelector('[data-lifecycle-photo]');

  const renderList = (node, items) => {
    if (!node) return;
    node.innerHTML = items.map((item) => `<li>${item}</li>`).join('');
  };

  const selectAge = (age) => {
    const content = lifecyclePersonas[age] || lifecyclePersonas['50s'];
    map.style.setProperty('--lifecycle-color', content.color);
    map.style.setProperty('--lifecycle-light', content.light);
    if (persona) persona.textContent = content.persona;
    if (about) about.textContent = content.about || '';
    renderList(miss, content.miss);
    renderList(adds, content.adds);
    renderList(adoption, content.adoption);
    if (photo && content.photo) {
      photo.src = content.photo;
      photo.alt = content.photoAlt;
    }
    tabs.forEach((tab) => {
      const selected = tab.dataset.lifecycleTab === age;
      tab.setAttribute('aria-selected', selected ? 'true' : 'false');
      tab.tabIndex = selected ? 0 : -1;
      tab.style.setProperty('--lifecycle-color', lifecyclePersonas[tab.dataset.lifecycleTab].color);
    });
  };

  // The section plays through the ages on its own until someone chooses one (2026-11-26).
  const panel = map.querySelector('[role="tabpanel"]');
  const stopAuto = () => {
    if (!map.classList.contains('is-auto')) return;
    map.classList.remove('is-auto');
    if (panel) panel.setAttribute('aria-live', 'polite');
  };
  const restartTimer = (tab) => {
    const timer = tab.querySelector('.ages-timer');
    if (!timer) return;
    const fresh = timer.cloneNode(true);
    timer.replaceWith(fresh);
    fresh.addEventListener('animationend', () => {
      if (!map.classList.contains('is-auto')) return;
      const index = tabs.indexOf(tab);
      const next = tabs[(index + 1) % tabs.length];
      selectAge(next.dataset.lifecycleTab);
      restartTimer(next);
    });
  };

  tabs.forEach((tab, index) => {
    tab.tabIndex = tab.getAttribute('aria-selected') === 'true' ? 0 : -1;
    tab.addEventListener('click', () => {
      stopAuto();
      selectAge(tab.dataset.lifecycleTab);
    });
    tab.addEventListener('keydown', (event) => {
      const step = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[event.key];
      if (!step) return;
      event.preventDefault();
      stopAuto();
      const next = tabs[(index + step + tabs.length) % tabs.length];
      selectAge(next.dataset.lifecycleTab);
      next.focus();
    });
  });

  selectAge(tabs[0].dataset.lifecycleTab);
  restartTimer(tabs[0]);

  // Play only while the section is on screen, starting from the first age when it first comes into view.
  if ('IntersectionObserver' in window) {
    new IntersectionObserver((entries) => {
      entries.forEach((entry) => map.classList.toggle('is-visible', entry.isIntersecting));
    }, { threshold: 0.35 }).observe(map);
  } else {
    map.classList.add('is-visible');
  }

  // Fetch the other age photos once the page has loaded, so switching tabs never shows an empty frame.
  if (photo) {
    window.addEventListener('load', () => {
      Object.values(lifecyclePersonas).forEach((content) => {
        if (content.photo) new Image().src = content.photo;
      });
    });
  }
});
