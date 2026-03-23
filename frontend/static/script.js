/* ── Guard: only runs on dashboard ─────────────── */
const uploadZone = document.getElementById('uploadZone');
if (!uploadZone) throw new Error('Not dashboard page.');

const $ = id => document.getElementById(id);
const imageInput   = $('imageInput');
const predictBtn   = $('predictBtn');
const imagePreview = $('imagePreview');
const previewWrap  = $('previewWrap');
const spinnerWrap  = $('spinnerWrap');
const spinnerText  = $('spinnerText');
const resultBox    = $('resultBox');
const errorBox     = $('errorBox');
const errorMsg     = $('errorMsg');
const diseaseText  = $('diseaseText');
const confPill     = $('confPill');
const confFill     = $('confFill');
const solutionText = $('solutionText');

let filename    = null;
let spinTimer   = null;

const MSGS = [
  'Scanning leaf texture…',
  'Checking vein patterns…',
  'Consulting disease database…',
  'Running AI diagnostics…',
  'Almost ready…',
];

/* ── Helpers ────────────────────────────────────── */
function setLoading(on) {
  spinnerWrap.classList.toggle('hidden', !on);
  predictBtn.disabled = on || !filename;
  if (on) {
    let i = 0;
    spinnerText.textContent = MSGS[0];
    spinTimer = setInterval(() => {
      spinnerText.textContent = MSGS[++i % MSGS.length];
    }, 1700);
  } else {
    clearInterval(spinTimer);
  }
}

function showError(msg) {
  errorMsg.textContent = msg;
  errorBox.classList.add('on');
}

function clearError() {
  errorMsg.textContent = '';
  errorBox.classList.remove('on');
}

function clearResult() {
  resultBox.classList.remove('on');
  diseaseText.textContent  = '—';
  confPill.textContent     = '—';
  confPill.className       = 'conf-tag';
  confFill.style.width     = '0%';
  solutionText.textContent = '—';
}

function resetPreview() {
  previewWrap.classList.remove('active');
  imagePreview.removeAttribute('src');
  filename = null;
  predictBtn.disabled = true;
}

/* ── Drag & drop ───────────────────────────────── */
uploadZone.addEventListener('dragover', e => {
  e.preventDefault();
  uploadZone.classList.add('over');
});
['dragleave','dragend'].forEach(ev =>
  uploadZone.addEventListener(ev, () => uploadZone.classList.remove('over'))
);
uploadZone.addEventListener('drop', e => {
  e.preventDefault();
  uploadZone.classList.remove('over');
  const f = e.dataTransfer?.files[0];
  if (f) handleFile(f);
});

/* ── File change ────────────────────────────────── */
imageInput.addEventListener('change', e => {
  const f = e.target.files[0];
  f ? handleFile(f) : resetPreview();
});

function handleFile(file) {
  filename = null;
  predictBtn.disabled = true;
  clearError();
  clearResult();

  if (!file.type.startsWith('image/')) {
    showError('Please choose a valid image file — JPG, PNG or WEBP.');
    return;
  }

  const reader = new FileReader();
  reader.onload = e => {
    imagePreview.src = e.target.result;
    previewWrap.classList.add('active');
  };
  reader.readAsDataURL(file);
  upload(file);
}

/* ── Upload ─────────────────────────────────────── */
async function upload(file) {
  setLoading(true);
  const form = new FormData();
  form.append('image', file);
  try {
    const res  = await fetch('/upload', { method: 'POST', body: form });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Upload failed.');
    filename = data.filename;
    predictBtn.disabled = false;
  } catch (err) {
    filename = null;
    predictBtn.disabled = true;
    showError(err.message || 'Upload failed.');
  } finally {
    setLoading(false);
  }
}

/* ── Predict ────────────────────────────────────── */
predictBtn.addEventListener('click', async () => {
  if (!filename) { showError('Please upload an image first.'); return; }

  clearError();
  clearResult();
  setLoading(true);

  try {
    const res  = await fetch('/predict', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ filename }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Prediction failed.');

    diseaseText.textContent  = data.disease  || 'Unknown';
    solutionText.textContent = data.solution || 'No recommendation available.';

    const raw   = data.confidence || '';
    const match = raw.match(/[\d.]+/);
    const num   = match ? parseFloat(match[0]) : NaN;
    const pct   = isNaN(num) ? null : (raw.includes('%') ? num : num * 100);

    confPill.textContent = raw || '—';
    if (pct !== null) {
      confPill.className = 'conf-tag ' + (pct >= 75 ? 'conf-hi' : pct >= 45 ? 'conf-md' : 'conf-lo');
      setTimeout(() => { confFill.style.width = Math.min(pct, 100) + '%'; }, 160);
    }

    resultBox.classList.add('on');
  } catch (err) {
    showError(err.message || 'Prediction failed.');
  } finally {
    setLoading(false);
  }
});