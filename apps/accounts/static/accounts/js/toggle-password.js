const input = document.getElementById('password');
const eyeOpen = document.querySelector('.auth__eye--open');
const eyeClosed = document.querySelector('.auth__eye--closed');

eyeOpen.onclick = eyeClosed.onclick = () => {
    const show = input.type === 'password';
    input.type = show ? 'text' : 'password';
    eyeOpen.style.display = show ? 'none' : 'block';
    eyeClosed.style.display = show ? 'block' : 'none';
};
