function apply_theme() {
  const existingTheme = document.querySelector("link[data-type='custom-theme']");
  if (existingTheme) {
    existingTheme.remove();
  }

  const theme = localStorage.getItem("theme");
  if (theme) {
    const link = document.createElement("link");
    link.setAttribute("rel", "stylesheet");
    link.setAttribute("type", "text/css");
    link.setAttribute("href", theme);
    link.setAttribute("data-type", "custom-theme");
    document.getElementsByTagName("head")[0].appendChild(link);
  }
}

apply_theme();