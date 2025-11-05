(function () {
  const savedTheme = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const isDark = savedTheme ? savedTheme === 'dark' : prefersDark;

  document.documentElement.classList.toggle('dark-theme', isDark);

  if (!savedTheme) {
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
  }
})();

document.addEventListener('DOMContentLoaded', () => {
  const toggleBtn = document.getElementById('theme-toggle');
  if (!toggleBtn) return;

  const savedTheme = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const isDark = savedTheme ? savedTheme === 'dark' : prefersDark;

  toggleBtn.checked = isDark;

  toggleBtn.addEventListener('change', () => {
    const isDarkNow = toggleBtn.checked;
    document.documentElement.classList.toggle('dark-theme', isDarkNow);
    localStorage.setItem('theme', isDarkNow ? 'dark' : 'light');
  });
});
