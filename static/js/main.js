
const hamburger = document.querySelector(".hamburger");
const navLinks = document.querySelector(".nav-links");
const links = document.querySelectorAll(".nav-links li");

hamburger.addEventListener("click", () => {
  navLinks.classList.toggle("open");
  hamburger.classList.toggle("open");
  links.forEach(link => {
    link.classList.toggle("fade");
  });
});

let loadSection = document.querySelector(".loader");

window.addEventListener("load", () => {
  loadSection.classList.toggle("finished");
});


let trigger = document.querySelector('#trigger-preloader');
let preLoadedr = document.querySelector('#preloader');

trigger.addEventListener('click', () => {
  preLoadedr.style.display = 'contents';
});

function vanish() {
  preLoadedr.style.display = 'none';
}

window.addEventListener("load", vanish());

