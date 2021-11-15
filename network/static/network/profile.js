const followBtn = document.querySelector("#follow");

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

if (followBtn) {
  followBtn.addEventListener("click", function () {
    const cookie = getCookie("csrftoken");

    const id = this.parentElement.dataset.id;
    fetch("/user/" + id, { method: "PUT", headers: header(cookie) })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        if (data.msg.toLowerCase().includes("you followed")) {
          followBtn.parentElement.querySelector(".followers").innerText =
            +followBtn.parentElement.querySelector(".followers").innerText + 1;
        } else {
          followBtn.parentElement.querySelector(".followers").innerText =
            +followBtn.parentElement.querySelector(".followers").innerText - 1;
        }
        //window.location.reload();
      })
      .catch((err) => {
        console.log(err);
      });
  });
}
