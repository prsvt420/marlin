const passwordInput = document.getElementById('password');
const openEyeIcon = document.querySelector('.form__eye--open');
const closedEyeIcon = document.querySelector('.form__eye--closed');

openEyeIcon.onclick = closedEyeIcon.onclick = () => {
  const isPasswordHidden = passwordInput.type === 'password';
  passwordInput.type = isPasswordHidden ? 'text' : 'password';
  openEyeIcon.style.display = isPasswordHidden ? 'none' : 'block';
  closedEyeIcon.style.display = isPasswordHidden ? 'block' : 'none';
};
