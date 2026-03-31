const inputPassword = document.getElementById("password");
const togglePassword = document.getElementById("toggle-password")
const eyeOpen = document.getElementById("eye-open");
const eyeClosed = document.getElementById("eye-closed");

togglePassword.addEventListener("click", () => {
  const isPasswordType = inputPassword.type === "password";
  inputPassword.type = isPasswordType ? "text" : "password";
  eyeOpen.classList.toggle("hidden", isPasswordType);
  eyeClosed.classList.toggle("hidden", !isPasswordType);
});
