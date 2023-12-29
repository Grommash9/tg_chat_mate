var modal = document.getElementById('user-settings-modal') as HTMLDivElement;
var btn = document.getElementById('user-save-settings') as HTMLButtonElement;
var span = document.getElementById('user-settings-close') as HTMLSpanElement;
const scriptToRemove = document.getElementById('user-settings-script-js');

span.onclick = function () {
  modal.style.display = 'none';
  modal.remove();
  if (scriptToRemove) {
    document.body.removeChild(scriptToRemove);
  }
};

window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = 'none';
    modal.remove();
    if (scriptToRemove) {
      document.body.removeChild(scriptToRemove);
    }
  }
};
