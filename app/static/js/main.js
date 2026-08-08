document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById("navToggle");
  const nav = document.getElementById("siteNav");

  if (!toggle || !nav) return;

  toggle.addEventListener("click", () => {
    const isOpen = nav.classList.toggle("open");
    toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const authPanel = document.getElementById("authPanel");
  if (!authPanel) return;

  document.querySelectorAll(".auth-toggle").forEach((btn) => {
    btn.addEventListener("click", () => {
      authPanel.setAttribute("data-view", btn.dataset.target);
    });
  });
});
