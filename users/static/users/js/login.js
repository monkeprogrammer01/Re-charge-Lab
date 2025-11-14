document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('main.auth-page form');
  const p1 = document.getElementById('regPwd');
  const p2 = document.getElementById('regPwd2');
  const err = document.getElementById('pwdErr');

  form.addEventListener('submit', e => {
    if (p1.value !== p2.value) {
      e.preventDefault(); // блокируем только если пароли не совпадают
      err.classList.add('show');
    } else {
      err.classList.remove('show'); // всё ок — отправляем форму
    }
  });
});
