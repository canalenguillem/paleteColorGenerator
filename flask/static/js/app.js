const form = document.querySelector("#form");
form.addEventListener("submit", function (e) {
  e.preventDefault();
  getColors();
});

function getColors() {
  const prompt = form.elements.prompt.value;
  console.log("prompt submited " + prompt);
  fetch("/paleta", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({
      prompt: prompt,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      const colors = data.colors;
      const container = document.querySelector(".container");
      createColorBoxes(colors, container);
    });
}

function createColorBoxes(colors, parent) {
  console.log("colors: " + colors);
  parent.textContent = "";
  for (const color of colors) {
    const div = document.createElement("div");
    div.classList.add("color");
    div.style.backgroundColor = color;
    div.style.width = `calc(100%/ ${colors.length})`;

    const span = document.createElement("span");
    span.textContent = color;
    div.appendChild(span);

    div.addEventListener("click", function () {
      navigator.clipboard.writeText(color);
    });

    parent.appendChild(div);
  }
}
