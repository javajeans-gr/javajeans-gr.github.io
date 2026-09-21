document.querySelectorAll('[data-year]').forEach((node) => {
  node.textContent = new Date().getFullYear();
});

document.querySelectorAll('form[data-contact-form]').forEach((form) => {
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const status = form.querySelector('[data-form-status]');
    if (status) {
      status.textContent = 'Preview mode: this will send through a protected server endpoint after deployment.';
    }
  });
});

const lifecyclePersonas = {
  '30s': {
    persona: 'Proactive tracker',
    color: '#14b8a6',
    light: '#f0fdfa',
    miss: [
      'Fitness apps track activity but ignore the connection between symptoms, labs, and recovery',
      'Wearables and monitors stay as siloed feeds without a unified risk story',
      'Generic health apps collect data but fail to notify care circles when baselines drift'
    ],
    adds: [
      'Intelligently combines personal profile info with trends from vitals and labs to detect risk',
      'Integrates wearables, Bluetooth cuffs, oximeters, scales, and camera vitals for a total view',
      'Establishes healthy baselines versus risk shifts to communicate next steps to the Star and care circle'
    ],
    adoption: ['Self-setup', 'Rich trend controls', 'Optional Angel later']
  },
  '40s': {
    persona: 'Household health manager',
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
    adoption: ['Fast setup', 'Household sharing', 'Clear low-friction notifications']
  },
  '50s': {
    persona: 'Chronic-risk planner',
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
    adoption: ['High-detail Star view', 'Guided setup option', 'Easy report sharing']
  },
  '60s': {
    persona: 'Transition',
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
    adoption: ['Guided setup', 'Readable controls', 'Fewer choices with optional Angel invitation']
  },
  '70s': {
    persona: 'Independent senior',
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
    adoption: ['Simple controls', 'Large targets', 'Defaults and Angel-assisted onboarding']
  },
  '80s': {
    persona: 'Higher-support senior',
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
    adoption: ['Angel-led setup', 'Passive capture', 'Maximum readability']
  }
};

document.querySelectorAll('[data-lifecycle-map]').forEach((map) => {
  const tabs = Array.from(map.querySelectorAll('[data-lifecycle-tab]'));
  const persona = map.querySelector('[data-lifecycle-persona]');
  const miss = map.querySelector('[data-lifecycle-miss]');
  const adds = map.querySelector('[data-lifecycle-adds]');
  const adoption = map.querySelector('[data-lifecycle-adoption]');

  const renderList = (node, items) => {
    if (!node) return;
    node.innerHTML = items.map((item) => `<li>${item}</li>`).join('');
  };

  const selectAge = (age) => {
    const content = lifecyclePersonas[age] || lifecyclePersonas['50s'];
    map.style.setProperty('--lifecycle-color', content.color);
    map.style.setProperty('--lifecycle-light', content.light);
    if (persona) persona.textContent = content.persona;
    renderList(miss, content.miss);
    renderList(adds, content.adds);
    renderList(adoption, content.adoption);
    tabs.forEach((tab) => {
      const selected = tab.dataset.lifecycleTab === age;
      tab.setAttribute('aria-selected', selected ? 'true' : 'false');
      tab.style.setProperty('--lifecycle-color', lifecyclePersonas[tab.dataset.lifecycleTab].color);
    });
  };

  tabs.forEach((tab) => {
    tab.addEventListener('click', () => selectAge(tab.dataset.lifecycleTab));
  });

  selectAge('50s');
});
