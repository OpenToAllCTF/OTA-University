const change_theme = (themeUrl) => {
  localStorage.setItem("theme", themeUrl);
  apply_theme();
};

const create_theme = (name, link) => {
  const entry = document.createElement("a");
  entry.classList.add("dropdown-item");
  entry.innerText = name;
  entry.onclick = () => change_theme(link);
  return entry;
};

const load_themes = async () => {
  const resp = await fetch("https://bootswatch.com/api/4.json");
  const data = await resp.json();
  const themesDiv = document.getElementById("theme-list");

  themesDiv.appendChild(create_theme("Default", ""));

  for (const theme of data.themes) {
    themesDiv.appendChild(create_theme(theme.name, theme.cssCdn));
  }

  const custom = create_theme("Custom", "");
  custom.onclick = () => change_theme(prompt("Enter a bootstrap theme url"));
  themesDiv.appendChild(custom);
};

$(document).ready(() => {
  load_themes();
});