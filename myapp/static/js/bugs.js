document
  .getElementById("showCommentFormBtn")
  .addEventListener("click", function () {
    document.getElementById("commentForm").style.display = "block";
  });

// JavaScript to close comment form
document
  .getElementById("closeCommentFormBtn")
  .addEventListener("click", function () {
    document.getElementById("commentForm").style.display = "none";
  });

document
  .getElementById("showRadioFormBtn")
  .addEventListener("click", function () {
    document.getElementById("radioForm").style.display = "block";
  });

// JavaScript to close radio button form
document
  .getElementById("closeRadioFormBtn")
  .addEventListener("click", function () {
    document.getElementById("radioForm").style.display = "none";
  });
