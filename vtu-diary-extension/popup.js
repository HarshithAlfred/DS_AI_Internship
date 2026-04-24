document.getElementById("fill").addEventListener("click", async () => {
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: fillForm
  });
});
document.getElementById("capture").addEventListener("click", async () => {
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: captureLMS
  });
});

document.getElementById("submit").addEventListener("click", async () => {
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: autoSubmit
  });
});
document.getElementById("save").addEventListener("click", async () => {
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: saveToday
  });
});

// ===== FUNCTIONS =====

function fillForm() {

  function selectOption(text) {
    const input = document.querySelector("input[id^='react-select']");
    if (!input) return;

    input.focus();
    input.value = text;
    input.dispatchEvent(new Event('input', { bubbles: true }));

    setTimeout(() => {
      input.dispatchEvent(new KeyboardEvent('keydown', {
        key: 'Enter',
        bubbles: true
      }));
    }, 200);
  }

  function generateFallback() {
    const topics = [
      "Model Deployment using Flask",
      "FastAPI basics",
      "Pipeline construction",
      "XGBoost training",
      "MLOps lifecycle"
    ];

    const topic = topics[Math.floor(Math.random() * topics.length)];

    return {
      work: `Worked on ${topic}. Implemented practical examples and improved understanding of real-world applications.`,
      hours: "6.5",
      reference: "https://github.com/harshithalfred",
      learning: `- Learned ${topic}\n- Improved debugging skills\n- Understood implementation flow`,
      blockers: `- Minor issues while working with ${topic}`,
      skills: [topic]
    };
  }

  chrome.storage.local.get(["yesterday", "lmsData"], (data) => {

    // priority: LMS → yesterday → fallback
    let entry = data.lmsData || data.yesterday;
    console.log(entry)
    if (!entry || !entry.work) {
      entry = generateFallback();
    }

    setValue("textarea[placeholder*='work']", entry.work);
    setValue("input[type='number']", entry.hours);
    setValue("textarea[placeholder*='links']", entry.reference);
    setValue("textarea[placeholder*='What did you learn or ship today?']", entry.learning);
    setValue("textarea[placeholder*='Anything that slowed you down?']", entry.blockers);

    // skills handling
    let values = ["Machine learning", "Python"];

    if (Array.isArray(entry.skills)) {
      values = values.concat(entry.skills);
    } else if (typeof entry.skills === "string" && entry.skills.length > 0) {
      values.push(entry.skills);
    }

    async function selectMultiple(values) {
      for (const v of values) {
        selectOption(v);
        await new Promise(res => setTimeout(res, 600));
      }
    }

    selectMultiple(values);

  });

  function setValue(selector, value) {
    const el = document.querySelector(selector);
    if (el) el.value = value;
  }

  function defaultEntry() {
    return {
      work: "Worked on MLOps concepts, explored FastAPI and pipeline construction.",
      hours: "7",
      reference: "https://github.com/harshithalfred",
      learning: "- Learned FastAPI basics\n- Understood MLOps workflow",
      blockers: "- Initial confusion in deployment concepts",
      skills: []
    };
  }
}

function saveToday() {
  const entry = {
    work: getValue("textarea[placeholder*='work']"),
    hours: getValue("input[type='number']"),
    reference: getValue("textarea[placeholder*='links']"),
    learning: getValue("textarea[placeholder*='learnings']"),
    blockers: getValue("textarea[placeholder*='blockers']"),
    skills: getValue("textarea[placeholder*='skills']")
  };

  chrome.storage.local.set({ yesterday: entry }, () => {
    alert("Saved as yesterday entry!");
  });

  function getValue(selector) {
    const el = document.querySelector(selector);
    return el ? el.value : "";
  }
}
function captureLMS() {
  const container = document.querySelector(".markdown-content");

  if (!container) {
    alert("LMS content not found!");
    return;
  }

  const paragraphs = Array.from(container.querySelectorAll("p"))
    .map(p => p.innerText.trim())
    .filter(p => p.length > 0);
console.log(p)
  let startIndex = paragraphs.findIndex(p =>
    p.toLowerCase().startsWith("today")
  );

  if (startIndex === -1) {
    alert("Could not find diary section!");
    return;
  }

  let work = paragraphs[startIndex];
  let hours = "4";
  let reference = "";
  let learning = "";
  let blockers = "";
  let skills = "";

  for (let i = startIndex + 1; i < paragraphs.length; i++) {
    const text = paragraphs[i];

    if (text.toLowerCase().includes("hours worked")) {
      const match = text.match(/[\d.]+/);
      if (match) hours = match[0];
    }

    else if (text.toLowerCase().includes("reference")) {
      // next paragraph will contain link
      reference = paragraphs[i + 1] || "";
    }

    else if (text.toLowerCase().includes("learnings")) {
      learning = paragraphs[i].replace(/learnings.*?/i, "").trim();

      // also include next few lines
      learning += "\n" + (paragraphs[i + 1] || "");
      learning += "\n" + (paragraphs[i + 2] || "");
    }

    else if (text.toLowerCase().includes("blockers")) {
      blockers = paragraphs[i].replace(/blockers.*?/i, "").trim();

      blockers += "\n" + (paragraphs[i + 1] || "");
      blockers += "\n" + (paragraphs[i + 2] || "");
    }

    else if (text.toLowerCase().includes("skills")) {
      skills = text.replace(/skills.*?/i, "").trim();
      break;
    }
  }

  const entry = {
    work,
    hours,
    reference,
    learning,
    blockers,
    skills
  };

  console.log("FINAL EXTRACT:", entry);

  chrome.storage.local.set({ lmsData: entry }, () => {
    alert("LMS data captured correctly!");
  });
}
// OPTIONAL: auto submit (call separately if needed)
function autoSubmit() {
  const btn = document.querySelector("button[type='submit']");
  if (!btn) {
    alert("Submit button not found!");
    return;
  }

  if (confirm("Submit diary entry?")) {
    btn.click();
  }
}