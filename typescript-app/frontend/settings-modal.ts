var modal = document.getElementById("settings-modal") as HTMLDivElement;
var btn = document.getElementById("manager-settings-button") as HTMLButtonElement;
var span = document.getElementsByClassName("close-button")[0] as HTMLSpanElement;

span.onclick = function() {
  modal.style.display = "none";
  modal.remove();
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

