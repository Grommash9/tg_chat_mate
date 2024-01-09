import { active_chat, User } from '../index.js';
import { UpdateUser, GetUser } from '../api_methods/user.js';

var modal = document.getElementById('user-settings-modal') as HTMLDivElement;
var span = document.getElementById('user-settings-close') as HTMLSpanElement;
const scriptToRemove = document.getElementById('user-settings-script-js');

span.onclick = function () {
  modal.style.display = 'none';
  modal.remove();
  if (scriptToRemove) {
    document.head.removeChild(scriptToRemove);
  }
};

window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = 'none';
    modal.remove();
    if (scriptToRemove) {
      document.head.removeChild(scriptToRemove);
    }
  }
};

GetShowUserData();

function GetShowUserData() {
  const UserDataDiv = document.getElementById(
    'user-data-container-object'
  ) as HTMLDivElement;
  UserDataDiv.innerHTML = '';

  GetUser(active_chat).then((user_info: User | null) => {
    if (user_info) {
      const photoObject = document.createElement('img');
      photoObject.classList.add('setting-user-photo');
      photoObject.width = 150;
      photoObject.height = 150;

      if (user_info.photo_uuid) {
        photoObject.src = '/tg-bot/file?file_uuid=' + user_info.photo_uuid;
      } else {
        photoObject.src = '/files/manager_empty_photo.png';
      }

      UserDataDiv.appendChild(photoObject);

      for (const [key, value] of Object.entries(user_info)) {
        console.log(`${key}: ${value}`);
        var label_holder = document.createElement('p');
        label_holder.className = `user_info_label_${key}`;
        label_holder.innerText = `${key}: ${value}`;

        if (UserDataDiv) {
          UserDataDiv.appendChild(label_holder);
        } else {
          console.log('Unable to find user-data-container-object!');
        }
      }

      var BanSwitchButton = document.createElement('button');
      UserDataDiv.appendChild(BanSwitchButton);

      if (user_info.is_banned) {
        BanSwitchButton.innerText = '🔓 UNBAN user';
        var payload = { is_banned: false };
      } else {
        BanSwitchButton.innerText = '🚫 BAN user';
        var payload = { is_banned: true };
      }
      BanSwitchButton.addEventListener('click', function () {
        UpdateUser(active_chat, payload);
        GetShowUserData();
      });
      console.log('User Info:', user_info);
    } else {
      console.log('Failed to get user info');
    }
  });
}
