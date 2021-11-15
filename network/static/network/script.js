const likeBtns = document.querySelectorAll(".like-btn");
const editBtn = document.querySelector(".edit");

if (editBtn) {
  editBtn.addEventListener("click", function () {
    const id = this.parentElement.dataset.id;
    const content = this.parentElement.querySelector("p").innerText;

    console.log("edit", id, content);
    this.classList.toggle("Show");
    if (this.classList.contains("Show")) {
      this.innerText = "Save";
      this.parentElement.style.display = "none";
      document.querySelector(`.editting ${id}`).style.display = "block";
    } else {
      this.innerText = "Edit";
    }
  });
}

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
          btn.innerText = "Like";
          btn.parentElement.querySelector("span").innerText =
            btn.parentElement.querySelector("span").innerText - 1;
        } else {
          btn.parentElement.querySelector("i").classList.add("text-danger");
          btn.innerText = "Dislike";
          btn.parentElement.querySelector("span").innerText =
            +btn.parentElement.querySelector("span").innerText + 1;
        }
      });
  });
});
