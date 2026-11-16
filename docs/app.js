const states = [
  "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
  "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
  "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri",
  "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York",
  "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island",
  "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
  "West Virginia", "Wisconsin", "Wyoming",
];

const services = {
  formation: {
    title: "LLC Formation",
    description: "Prepare a business name, confirm your filing state, and gather the details needed to file.",
    checklist: [
      "Check your proposed business name with the state filing office.",
      "Decide who will act as the registered agent and confirm their details.",
      "Review the official filing instructions and ask for an itemized setup quote.",
    ],
  },
  agent: {
    title: "Registered Agent",
    description: "Review providers in the state where your business will be registered.",
    checklist: [
      "Confirm the provider covers your formation state.",
      "Ask about the renewal price and how you’ll receive official documents.",
      "Check your formation documents before appointing or changing an agent.",
    ],
  },
  ein: {
    title: "EIN Assistance",
    description: "Prepare your business details and review the official IRS application instructions.",
    checklist: [
      "Confirm the exact legal name and formation details of your company.",
      "Identify the responsible party for the application.",
      "Check which IRS application route applies before sharing any personal information.",
    ],
  },
  unsure: {
    title: "Help me choose",
    description: "Start with the business setup task you need to complete first.",
    checklist: [
      "Write down where you plan to operate and whether you have already formed your company.",
      "Review the LLC formation and registered agent service options.",
      "List the questions you want answered before paying for a package.",
    ],
  },
};

const dialog = document.querySelector("#dialog");
const title = document.querySelector("#dialog-title");
const content = document.querySelector("#dialog-content");
const form = document.querySelector("#setup");
const stateSelect = document.querySelector("#state");
const serviceSelect = document.querySelector("#service");

for (const state of states) stateSelect.add(new Option(state, state));

function showDialog(heading) {
  title.textContent = heading;
  content.replaceChildren();
  dialog.showModal();
}

function addText(tag, text, className) {
  const element = document.createElement(tag);
  element.textContent = text;
  if (className) element.className = className;
  content.append(element);
  return element;
}

function setState(state) {
  stateSelect.value = state;
  if (dialog.open) dialog.close();
  serviceSelect.focus();
}

document.querySelector("#all-states").addEventListener("click", () => {
  showDialog("Choose a formation state");
  const list = addText("div", "", "state-grid");
  for (const state of states) {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = state;
    button.addEventListener("click", () => setState(state));
    list.append(button);
  }
  list.firstElementChild.focus();
});

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const service = services[serviceSelect.value];
  showDialog("Your setup checklist");
  const state = stateSelect.value === "Undecided" ? "State undecided" : stateSelect.value;
  addText("p", state + " · " + service.title);
  const list = addText("ul", "");
  for (const step of service.checklist) {
    const item = document.createElement("li");
    item.textContent = step;
    list.append(item);
  }
  addText("p", "This checklist has not been sent to a provider.", "dialog-note");
});
