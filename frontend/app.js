/**
 * UberFare AI — app.js
 * XGBoost Model Prediction Frontend
 */

const $ = id => document.getElementById(id);

const el = {
  form:             $('fareForm'),
  distanceKm:       $('distanceKm'),
  durationMin:      $('durationMin'),
  vehicleType:      $('vehicleType'),
  trafficLevel:     $('trafficLevel'),
  roadType:         $('roadType'),
  stopsAdded:       $('stopsAdded'),
  pickupArea:       $('pickupArea'),
  dropArea:         $('dropArea'),
  timeSlot:         $('timeSlot'),
  dayType:          $('dayType'),
  weatherCond:      $('weatherCond'),
  rainfall:         $('rainfall'),
  tempLevel:        $('tempLevel'),
  busyDay:          $('busyDay'),
  holiday:          $('holiday'),
  calcBtn:          $('calcBtn'),
  calcBtnLabel:     $('calcBtnLabel'),
  errorBanner:      $('errorBanner'),
  errorMsg:         $('errorMsg'),
  resultsPanel:     $('resultsPanel'),
  dialogBackdrop:   $('dialogBackdrop'),
  openDialogBtn:    $('openDialogBtn'),
  closeDialogBtn:   $('closeDialogBtn'),
  fareAmount:       $('fareAmount'),
  fareMin:          $('fareMin'),
  fareMax:          $('fareMax'),
  rideBadge:        $('rideBadge'),
};

document.addEventListener('DOMContentLoaded', () => {
  el.resultsPanel.hidden = true;
  bindEvents();
  openDialog();
});

function bindEvents() {
  el.form.addEventListener('submit', e => {
    e.preventDefault();
    calculateFare();
  });

  el.openDialogBtn.addEventListener('click', openDialog);
  el.closeDialogBtn.addEventListener('click', closeDialog);

  el.dialogBackdrop.addEventListener('click', e => {
    if (e.target === el.dialogBackdrop) closeDialog();
  });

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && !el.dialogBackdrop.hidden) closeDialog();
  });
}

function openDialog() {
  hideError();
  el.dialogBackdrop.hidden = false;
  document.body.classList.add('dialog-open');
  requestAnimationFrame(() => {
    el.dialogBackdrop.classList.add('is-open');
  });
}

function closeDialog() {
  el.dialogBackdrop.classList.remove('is-open');
  document.body.classList.remove('dialog-open');
  setTimeout(() => {
    el.dialogBackdrop.hidden = true;
  }, 200);
}

async function reloadModel() {
  const btn = document.getElementById('reloadModelBtn');
  btn.textContent = 'Reloading…';
  btn.disabled = true;
  try {
    const res = await fetch('/api/reload', { method: 'POST' });
    const data = await res.json();
    if (data.success) {
      btn.textContent = 'Reloaded';
      btn.style.color = '#059669';
      showToast(`Model reloaded (saved: ${data.model_last_modified})`);
      setTimeout(() => {
        btn.textContent = 'Reload Model';
        btn.style.color = '';
        btn.disabled = false;
      }, 3000);
    } else {
      throw new Error(data.error);
    }
  } catch (err) {
    btn.textContent = 'Failed';
    btn.style.color = '#e11d48';
    setTimeout(() => {
      btn.textContent = 'Reload Model';
      btn.style.color = '';
      btn.disabled = false;
    }, 3000);
  }
}

function showToast(msg) {
  let toast = document.getElementById('reloadToast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'reloadToast';
    toast.style.cssText = 'transform:translateY(80px);opacity:0;transition:all 0.3s ease;';
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  setTimeout(() => { toast.style.transform = 'translateY(0)'; toast.style.opacity = '1'; }, 10);
  setTimeout(() => { toast.style.transform = 'translateY(80px)'; toast.style.opacity = '0'; }, 4000);
}

async function calculateFare() {
  hideError();

  const distance_km   = parseFloat(el.distanceKm.value) || 15.0;
  const duration_min  = parseFloat(el.durationMin.value) || 25.0;
  const vehicle_type  = el.vehicleType.value;
  const traffic_level = parseInt(el.trafficLevel.value, 10);
  const road_type     = el.roadType.value;
  const stops_added   = parseFloat(el.stopsAdded.value) || 0;
  const pickup_area   = el.pickupArea.value;
  const drop_area     = el.dropArea.value;
  const time_slot     = el.timeSlot.value;
  const day_type      = parseInt(el.dayType.value, 10);
  const weather_cond  = parseInt(el.weatherCond.value, 10);
  const rainfall      = parseInt(el.rainfall.value, 10);
  const temp_level    = parseInt(el.tempLevel.value, 10);
  const busy_day      = el.busyDay.value;
  const holiday       = parseInt(el.holiday.value, 10);

  el.calcBtn.disabled = true;
  el.calcBtnLabel.textContent = 'Predicting…';

  try {
    const payload = {
      distance_km,
      duration_min,
      vehicle_type,
      traffic_level,
      road_type,
      number_of_stops: stops_added,
      pickup_area_type: pickup_area,
      drop_area_type: drop_area,
      time_slot,
      day_type,
      weather_condition: weather_cond,
      rainfall_intensity: rainfall,
      temperature_level: temp_level,
      busy_day,
      holiday
    };

    const res = await fetch('/api/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!res.ok) throw new Error(`Server returned HTTP ${res.status}`);

    const data = await res.json();
    if (!data.success) throw new Error(data.error || 'Prediction failed');

    renderResults(data.predicted_fare, payload);
    el.resultsPanel.hidden = false;
    closeDialog();

  } catch (err) {
    showError(err.message || 'Error communicating with XGBoost Backend API.');
  } finally {
    el.calcBtn.disabled = false;
    el.calcBtnLabel.textContent = 'Predict Fare';
  }
}

function renderResults(fare, payload) {
  el.rideBadge.textContent = payload.vehicle_type;

  animateMoney(el.fareAmount, 0, fare, 700);
  el.fareMin.textContent = fmtRs(fare * 0.90);
  el.fareMax.textContent = fmtRs(fare * 1.15);
}

function showError(msg) {
  el.errorBanner.hidden = false;
  el.errorMsg.textContent = msg;
}
function hideError() {
  el.errorBanner.hidden = true;
}

function fmtRs(val) {
  return '\u20b9 ' + Math.round(val || 0).toLocaleString('en-IN');
}

function animateMoney(el2, from, to, duration) {
  const start = performance.now();
  const update = now => {
    const t = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - t, 3);
    el2.textContent = (from + (to - from) * eased).toFixed(2);
    if (t < 1) requestAnimationFrame(update);
  };
  requestAnimationFrame(update);
}
