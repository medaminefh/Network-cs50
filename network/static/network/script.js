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

likeBtns.forEach((btn) => {
  const id = btn.parentElement.dataset.id;

  btn.addEventListener("click", () => {
    fetch("/like/" + id)
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        window.location.reload();
      });
  });
});
