const likeBtns = document.querySelectorAll(".like-btn");

likeBtns.forEach((btn) => {
  const id = btn.parentElement.parentElement.dataset.id;
  btn.addEventListener("submit", function (e) {
    e.preventDefault();
    fetch("/like", {
      method: "POST",
      body: JSON.stringify({
        tweetId: id,
      }),
    })
      .then((res) => res.json)
      .then((data) => console.log(data));
  });
});
