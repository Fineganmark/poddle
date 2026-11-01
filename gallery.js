/* Stop-page photo gallery: picking a thumbnail shows that photo large, with its caption.
   Without JavaScript the thumbnails are plain links to the full-size photos. */
(function () {
  var boxes = document.querySelectorAll(".gallery");
  for (var b = 0; b < boxes.length; b++) (function (box) {
    var big = box.querySelector(".gal-stage img"), cap = box.querySelector(".gal-cap");
    var thumbs = box.querySelectorAll(".gal-thumb");
    for (var k = 0; k < thumbs.length; k++) {
      thumbs[k].addEventListener("click", function (e) {
        e.preventDefault();
        big.src = this.getAttribute("href");
        big.alt = cap.textContent = this.getAttribute("data-cap");
        for (var j = 0; j < thumbs.length; j++) thumbs[j].removeAttribute("aria-current");
        this.setAttribute("aria-current", "true");
      });
    }
  })(boxes[b]);
})();
