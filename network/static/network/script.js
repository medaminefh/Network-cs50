const likeBtns = document.querySelectorAll(".like-btn");

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
