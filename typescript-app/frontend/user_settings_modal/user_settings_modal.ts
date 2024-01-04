import { active_chat, User } from '../index.js';
import { UpdateUser, GetUser } from '../api_methods/user.js';

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

ShowUserData();


function ShowUserData() {
  let user_data = GetUser(active_chat);

  GetUser(active_chat).then((user_info: User | null) => {
    if (user_info) {
      console.log('User Info:', user_info);
    } else {
      console.log('Failed to get user info');
    }
  });
};
