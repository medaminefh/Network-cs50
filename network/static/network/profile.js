const followBtn = document.querySelector("#follow");

followBtn.addEventListener("click", function () {
  const id = this.parentElement.dataset.id;

  fetch("/user/" + Number(id))
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
      //window.location.reload();
    });
});
