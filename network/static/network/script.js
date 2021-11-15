const likeBtns = document.querySelectorAll(".like-btn");

function getCookie(cname) {
  let name = cname + "=";
  let ca = document.cookie.split(";");
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == " ") {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

const header = (cookie) => ({
  Accept: "application/json, text/plain, */*",
  "Content-Type": "application/json",
  "X-CSRFToken": cookie,
});

likeBtns.forEach((btn) => {
  const id = btn.parentElement.dataset.id;

  btn.addEventListener("click", () => {
    const cookie = getCookie("csrftoken");
    fetch("/like/" + id, { method: "PUT", headers: header(cookie) })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        if (data.Success == "Disliked") {
          btn.parentElement.querySelector("i").classList.remove("text-danger");
          btn.parentElement.querySelector("span").innerText =
            btn.parentElement.querySelector("span").innerText - 1;
        } else {
          btn.parentElement.querySelector("i").classList.add("text-danger");
          btn.parentElement.querySelector("span").innerText =
            +btn.parentElement.querySelector("span").innerText + 1;
        }
      });
  });
});
