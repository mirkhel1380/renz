const renzStates = [
  "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
  "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
  "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri",
  "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York",
  "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island",
  "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
  "West Virginia", "Wisconsin", "Wyoming",
];

function makeStateDirectory(root) {
  const search = root.querySelector("input");
  const list = root.querySelector("ul");
  const empty = root.querySelector("[role='status']");
  const path = root.dataset.home;
  for (const name of renzStates) {
    const row = document.createElement("li");
    const link = document.createElement("a");
    link.href = path + "?state=" + encodeURIComponent(name) + "#setup";
    link.textContent = name;
    row.append(link);
    list.append(row);
  }

  search.addEventListener("input", () => {
    const query = search.value.trim().toLowerCase();
    let visible = 0;
    for (const row of list.children) {
      row.hidden = !row.textContent.toLowerCase().includes(query);
      if (!row.hidden) visible += 1;
    }
    empty.textContent = visible ? "" : "No states match your search.";
  });
}

const directoryRoot = document.querySelector("[data-state-directory]");
if (directoryRoot) makeStateDirectory(directoryRoot);
