const SIDEBAR_KEY = "adminHMD.sidebarMini";
const THEME_KEY = "adminHMD.colorTheme";
const DESKTOP_MEDIA = "(min-width: 992px)";

const ready = (fn) => {
  if (document.readyState !== "loading") fn();
  else document.addEventListener("DOMContentLoaded", fn);
};

const isDesktop = () =>
  window.matchMedia(DESKTOP_MEDIA).matches;

const safeStorage = (() => {
  try {
    const key = "__test__";
    localStorage.setItem(key, "1");
    localStorage.removeItem(key);
    return localStorage;
  } catch {
    return null;
  }
})();

const storage = {
  get(key) {
    return safeStorage?.getItem(key);
  },
  set(key, value) {
    safeStorage?.setItem(key, value);
  },
};

const debounce = (fn, delay = 200) => {
  let t;
  return (...args) => {
    clearTimeout(t);
    t = setTimeout(() => fn(...args), delay);
  };
};

/* ---------------- THEME ---------------- */

function getPreferredTheme() {
  const saved = storage.get(THEME_KEY);

  if (saved === "dark" || saved === "light") return saved;

  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
}

function applyTheme(theme, els) {
  document.documentElement.dataset.theme = theme;
  document.documentElement.dataset.bsTheme = theme;

  storage.set(THEME_KEY, theme);

  const next = theme === "dark" ? "light" : "dark";
  const label = `Switch to ${next} mode`;
  const icon = theme === "dark" ? "bi bi-sun" : "bi bi-moon-stars";

  els.toggles.forEach((btn) => {
    btn.setAttribute("aria-label", label);
    btn.setAttribute("title", label);
  });

  els.icons.forEach((i) => {
    i.className = icon;
  });
}

function initTheme() {
  const toggles = document.querySelectorAll("[data-theme-toggle]");
  const icons = document.querySelectorAll("[data-theme-icon]");

  const els = { toggles, icons };

  applyTheme(getPreferredTheme(), els);

  toggles.forEach((btn) => {
    btn.addEventListener("click", () => {
      const current = document.documentElement.dataset.theme || "light";
      applyTheme(current === "dark" ? "light" : "dark", els);
    });
  });
}

/* ---------------- VALIDATION ---------------- */

function initValidation() {
  document.querySelectorAll(".needs-validation").forEach((form) => {
    form.addEventListener("submit", (e) => {
      if (!form.checkValidity()) {
        e.preventDefault();
        e.stopPropagation();
      }
      form.classList.add("was-validated");
    });
  });
}

/* ---------------- TABLE SEARCH ---------------- */

function initTableSearch() {
  document.querySelectorAll("[data-table-search]").forEach((input) => {
    const tableId = input.dataset.tableSearch;
    const table = document.getElementById(tableId);
    if (!table) return;

    const rows = Array.from(table.querySelectorAll("tbody tr"));

    const filter = debounce(() => {
      const q = input.value.trim().toLowerCase();

      rows.forEach((row) => {
        row.hidden = q && !row.textContent.toLowerCase().includes(q);
      });
    }, 150);

    input.addEventListener("input", filter);
  });
}

/* ---------------- USER PROFILE ---------------- */

function initUserProfile() {
  const user = window.adminHMDUser ?? {
    name: "Admin Hasan",
    workspace: "Active Workspace",
    avatar: "/../images/avatar/avatar.jpg",
  };

  const sidebarName = document.querySelector(".sidebar-user strong");
  const sidebarWorkspace = document.querySelector(".sidebar-user small");
  const sidebarAvatar = document.querySelector(".sidebar-user .avatar-img");

  const names = document.querySelectorAll(".profile-name");
  const avatars = document.querySelectorAll(
    ".profile-button .avatar-img, .profile-button img"
  );

  if (sidebarName) sidebarName.textContent = user.name;
  if (sidebarWorkspace) sidebarWorkspace.textContent = user.workspace;

  if (sidebarAvatar && user.avatar) {
    sidebarAvatar.src = user.avatar;
    sidebarAvatar.alt = user.name;
  }

  names.forEach((el) => (el.textContent = user.name));

  avatars.forEach((img) => {
    if (user.avatar) img.src = user.avatar;
    if (user.name) img.alt = user.name;
  });
}

/* ---------------- SIDEBAR ---------------- */

function initSidebar() {
  const body = document.body;
  const toggle = document.querySelector("[data-sidebar-toggle]");
  if (!toggle) return;

  const closeEls = document.querySelectorAll(
    "[data-sidebar-close], .sidebar-nav .nav-link"
  );

  const media = window.matchMedia(DESKTOP_MEDIA);

  const getMini = () =>
    storage.get(SIDEBAR_KEY) === "true";

  const setExpanded = () => {
    const expanded = isDesktop()
      ? !body.classList.contains("sidebar-mini")
      : body.classList.contains("sidebar-open");

    toggle.setAttribute("aria-expanded", String(expanded));
  };

  const saveMini = (val) => storage.set(SIDEBAR_KEY, String(val));

  const closeMobile = () => {
    body.classList.remove("sidebar-open");
    setExpanded();
  };

  const toggleSidebar = () => {
    if (isDesktop()) {
      body.classList.toggle("sidebar-mini");
      saveMini(body.classList.contains("sidebar-mini"));
    } else {
      body.classList.toggle("sidebar-open");
    }

    setExpanded();
  };

  const handleBreakpoint = () => {
    if (isDesktop()) {
      body.classList.remove("sidebar-open");
      if (getMini()) body.classList.add("sidebar-mini");
    } else {
      body.classList.remove("sidebar-mini");
    }

    setExpanded();
  };

  const bindClose = (el) =>
    el.addEventListener("click", () => {
      if (!isDesktop()) closeMobile();
    });

  if (getMini() && isDesktop()) {
    body.classList.add("sidebar-mini");
  }

  toggle.addEventListener("click", toggleSidebar);
  closeEls.forEach(bindClose);

  setExpanded();

  if (media.addEventListener) {
    media.addEventListener("change", handleBreakpoint);
  } else {
    media.addListener(handleBreakpoint);
  }
}

/* ---------------- INIT ---------------- */

ready(() => {
  initValidation();
  initTableSearch();
  initTheme();
//  initUserProfile();
  initSidebar();
});