document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('main.auth-page form');
  const pwd1 = document.getElementById('regPwd');
  const pwd2 = document.getElementById('regPwd2');
  const err = document.getElementById('pwdErr');
  const submitBtn = document.getElementById('regSubmit');

  const checkPasswords = () => {
    if (pwd2.value === "" || pwd1.value === pwd2.value) {
      err.classList.remove('show');
      submitBtn.disabled = false;
      pwd2.setCustomValidity('');
    } else {
      err.classList.add('show');
      submitBtn.disabled = true;
      pwd2.setCustomValidity('Passwords do not match');
    }
  };

  pwd1.addEventListener('input', checkPasswords);
  pwd2.addEventListener('input', checkPasswords);

  form.addEventListener('submit', (e) => {
    checkPasswords();
  });
});
