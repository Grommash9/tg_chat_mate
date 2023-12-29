var modal = document.getElementById('settings-modal') as HTMLDivElement;
var btn = document.getElementById(
  'manager-settings-button'
) as HTMLButtonElement;
var span = document.getElementById('close-manager-settings') as HTMLSpanElement;
const jsScriptToRemove = document.getElementById('manager-settings-script-js');

span.onclick = function () {
  modal.style.display = 'none';
  modal.remove();
  if (jsScriptToRemove) {
    document.body.removeChild(jsScriptToRemove);
  }
};

window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = 'none';
    modal.remove();
    if (jsScriptToRemove) {
      document.body.removeChild(jsScriptToRemove);
    }
  }
};
