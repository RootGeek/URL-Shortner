document.addEventListener("DOMContentLoaded", () => {
  // Theme is fixed to dark mode; no toggle.
  const html = document.documentElement;
  if (!html.classList.contains("dark")) {
    html.classList.add("dark");
  }
});
