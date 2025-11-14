document.addEventListener('DOMContentLoaded', () => {
  const forms = document.querySelectorAll('main.auth-page form');
  forms.forEach(form => {
    form.addEventListener('submit', e => {
      e.preventDefault();
    });
  });

  const pwdInput = document.getElementById('pwd');
  const eyeBtn = document.querySelector('.eye');

  if (pwdInput && eyeBtn) {
    eyeBtn.addEventListener('click', () => {
      pwdInput.type = pwdInput.type === 'password' ? 'text' : 'password';
    });
  }

  const p1 = document.getElementById('regPwd');
  const p2 = document.getElementById('regPwd2');
  const err = document.getElementById('pwdErr');
  const submit = document.getElementById('regSubmit');

  if (p1 && p2 && err && submit) {
    const checkMatch = () => {
      const ok = p2.value.length === 0 || p1.value === p2.value;
      err.classList.toggle('show', !ok);
      submit.disabled = !ok;
      p2.setCustomValidity(ok ? '' : 'Passwords do not match.');
    };

    p1.addEventListener('input', checkMatch);
    p2.addEventListener('input', checkMatch);
  }
});
