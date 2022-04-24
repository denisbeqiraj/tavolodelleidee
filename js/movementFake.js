

const img = document.getElementById("imm");
img.addEventListener("error", myFunction());

function myFunction() {
  var text = document.createElement("div");
  text.className = "text";
  text.innerHTML = "Lavoro di semestre di Natalia Andaloro e Denis Beqiraj";
  var parent = img.parentNode;
  parent.insertBefore(text,img);
  parent.removeChild(img);
}