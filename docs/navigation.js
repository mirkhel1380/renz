const siteHeader = document.querySelector("[data-site-header]");
const menuToggle = siteHeader.querySelector(".menu-toggle");
const mainNavigation = siteHeader.querySelector(".main-nav");
const dropdowns = [...mainNavigation.querySelectorAll("details")];

siteHeader.dataset.enhanced = "true";

function setMobileMenu(expanded) {
  menuToggle.setAttribute("aria-expanded", String(expanded));
  siteHeader.dataset.menuOpen = String(expanded);
}

function closeMenus() {
  for (const dropdown of dropdowns) dropdown.open = false;
}

menuToggle.addEventListener("click", () => {
  const willOpen = menuToggle.getAttribute("aria-expanded") !== "true";
  setMobileMenu(willOpen);
  if (!willOpen) closeMenus();
});

mainNavigation.addEventListener("click", (event) => {
  if (event.target.closest("a")) {
    closeMenus();
    setMobileMenu(false);
  }
});

document.addEventListener("click", (event) => {
  if (!siteHeader.contains(event.target)) {
    closeMenus();
    setMobileMenu(false);
  }
});

siteHeader.addEventListener("keydown", (event) => {
  if (event.key !== "Escape") return;
  const open = dropdowns.find((dropdown) => dropdown.open);
  if (open) {
    open.open = false;
    open.querySelector("summary").focus();
    event.preventDefault();
  } else if (menuToggle.getAttribute("aria-expanded") === "true") {
    setMobileMenu(false);
    menuToggle.focus();
    event.preventDefault();
  }
});

const smallHeader = window.matchMedia("(max-width: 900px)");
smallHeader.addEventListener("change", () => {
  setMobileMenu(false);
  closeMenus();
});
