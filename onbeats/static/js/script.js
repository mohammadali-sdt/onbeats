// MenuView Open and Close
const menuView = document.querySelector(".menuView");
const menuView__cross = document.querySelector(".menuView__cross");
const menuIcon = document.querySelector(".heroImage__menu");

menuIcon.addEventListener("click", function (e) {
  e.preventDefault();
  menuView.classList.add("menuView--open");
});

menuView__cross.addEventListener("click", function (e) {
  e.preventDefault();
  menuView.classList.remove("menuView--open");
});
