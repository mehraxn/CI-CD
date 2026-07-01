// Footer status bar reflects the /health endpoint response.
// Lives in a static file (not inline) so the Content-Security-Policy can
// remain strict: default-src 'self' with no 'unsafe-inline'.
(function () {
  var bar = document.querySelector(".statusbar");
  var dot = document.getElementById("health-dot");
  var value = document.getElementById("health-value");
  if (!bar || !dot || !value) return;

  fetch(bar.dataset.healthUrl || "/health")
    .then(function (r) {
      return r.json();
    })
    .then(function (data) {
      value.textContent = JSON.stringify(data);
      dot.classList.add(data.status === "ok" ? "is-ok" : "is-bad");
    })
    .catch(function () {
      value.textContent = "unreachable";
      dot.classList.add("is-bad");
    });
})();
