const likeBtns = document.querySelectorAll(".like-btn");
const editBtns = document.querySelectorAll(".edit");

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

const cookie = getCookie("csrftoken");

if (editBtns) {
  editBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      const id = this.parentElement.dataset.id;
      document.querySelector(".hide_" + id).style.display = "block";
      document.querySelector(".show_" + id).style.display = "none";
      if (document.querySelector(".hide_" + id + " textarea").value == "") {
        document.querySelector(".hide_" + id + " textarea").value = document
          .querySelector(".show_" + id + " p")
          .innerText.trim();
      }

      document.querySelector(".return_" + id).addEventListener("click", () => {
        document.querySelector(".hide_" + id + " h4").innerText = "";
        if (document.querySelector(".hide_" + id + " textarea").value == "") {
          document.querySelector(".hide_" + id + " textarea").value = document
            .querySelector(".show_" + id + " p")
            .innerText.trim();
        }
        document.querySelector(".hide_" + id).style.display = "none";
        document.querySelector(".show_" + id).style.display = "block";
      });

      document.querySelector(".save_" + id).addEventListener("click", () => {
        const content = document.querySelector(
          ".hide_" + id + " .content"
        ).value;

        fetch("/tweet/" + id, {
          method: "PUT",
          headers: header(cookie),
          body: JSON.stringify({ content }),
        })
          .then((res) => res.json())
          .then((data) => {
            if (!data.error) {
              document.querySelector(".hide_" + id + " h4").innerText = "";
              document.querySelector(".show_" + id + " p").innerText = content;
              document.querySelector(".hide_" + id).style.display = "none";
              document.querySelector(".show_" + id).style.display = "block";
            } else {
              document.querySelector(".hide_" + id + " h4").innerText =
                data.error;
            }
          })
          .catch((err) => console.log(err));
      });
    });
  });
}

likeBtns.forEach((btn) => {
  const id = btn.parentElement.dataset.id;

  btn.addEventListener("click", () => {
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
