import { getManager, getAllManagers } from '../api_methods/get_manager_info.js';
import { Manager } from '../index.js';

var modal = document.getElementById('settings-modal') as HTMLDivElement;
var btn = document.getElementById(
  'manager-settings-button'
) as HTMLButtonElement;
var span = document.getElementById('close-manager-settings') as HTMLSpanElement;
const jsScriptToRemove = document.getElementById('manager-settings-script-js');

btn.onclick = function () {
  closeManagerSettings();
};

span.onclick = function () {
  closeManagerSettings();
};

window.onclick = function (event) {
  if (event.target == modal) {
    closeManagerSettings();
  }
};

function closeManagerSettings() {
  modal.style.display = 'none';
  modal.remove();
  if (jsScriptToRemove) {
    document.body.removeChild(jsScriptToRemove);
  }
}

const my_profile_button = document.getElementById(
  'manager-setting-my-profile'
) as HTMLParagraphElement;
const managers_management_button = document.getElementById(
  'manager-setting-manager-settings'
) as HTMLParagraphElement;
const global_setting_button = document.getElementById(
  'manager-setting-global-settings'
) as HTMLParagraphElement;
const any_settings_button = document.getElementById(
  'manager-setting-any-settings'
) as HTMLParagraphElement;
const lang_settings_button = document.getElementById(
  'manager-setting-lang-settings'
) as HTMLParagraphElement;
const qa_settings_button = document.getElementById(
  'manager-setting-qa-settings'
) as HTMLParagraphElement;
const start_message_button = document.getElementById(
  'manager-setting-start-message'
) as HTMLParagraphElement;
const data_management_button = document.getElementById(
  'manager-setting-data-management'
) as HTMLParagraphElement;
const settingContent = document.getElementById(
  'settings-content-object'
) as HTMLDivElement;

if (my_profile_button) {
  my_profile_button.addEventListener('click', displayMyProfileSettings);
}

if (managers_management_button) {
  managers_management_button.addEventListener('click', DisplayManagerManagementSettings);
}

if (global_setting_button) {
  global_setting_button.addEventListener('click', notImplementedHandler);
}

if (any_settings_button) {
  any_settings_button.addEventListener('click', notImplementedHandler);
}

if (start_message_button) {
  start_message_button.addEventListener('click', notImplementedHandler);
}

if (lang_settings_button) {
  lang_settings_button.addEventListener('click', notImplementedHandler);
}

if (qa_settings_button) {
  qa_settings_button.addEventListener('click', notImplementedHandler);
}

if (data_management_button) {
  data_management_button.addEventListener('click', notImplementedHandler);
}

async function DisplayManagerManagementSettings() {
  cleanUpSettings();

  managers_management_button.style.backgroundColor = '#00ff70';

  
  var managers_list = await getAllManagers();
  managers_list.forEach(manager => {

    const managerSettings = document.createElement('div');

    const photoObject = document.createElement('img');
    photoObject.classList.add('setting-user-photo');
    photoObject.width = 50;
    photoObject.height = 50;

    if (manager.photo_uuid) {
      photoObject.src = '/tg-bot/file?file_uuid=' + manager.photo_uuid;
    } else {
      photoObject.src = '/files/manager_empty_photo.png';
    }

    managerSettings.appendChild(photoObject);
    
    const managerUserName = document.createElement('p');
    managerUserName.innerText = manager.username;

    managerSettings.appendChild(managerUserName);

    const managerFullName = document.createElement('p');
    managerFullName.innerText = manager.full_name;

    managerSettings.appendChild(managerFullName);
    settingContent.appendChild(managerSettings);


  });
  
}

async function displayMyProfileSettings() {
  cleanUpSettings();

  my_profile_button.style.backgroundColor = '#00ff70';

  var manager: Manager = await getManager();
  console.log(manager);
  if (manager) {
    const photoObject = document.createElement('img');
    photoObject.classList.add('setting-user-photo');
    photoObject.width = 150;
    photoObject.height = 150;

    if (manager.photo_uuid) {
      photoObject.src = '/tg-bot/file?file_uuid=' + manager.photo_uuid;
    } else {
      photoObject.src = '/files/manager_empty_photo.png';
    }

    settingContent.appendChild(photoObject);
  }

  const managerUserName = document.createElement('p');
  managerUserName.innerText = manager.username;

  settingContent.appendChild(managerUserName);

  const managerFullName = document.createElement('p');
  managerFullName.innerText = manager.full_name;

  settingContent.appendChild(managerFullName);
}

function notImplementedHandler(event: MouseEvent) {
  cleanUpSettings();

  const clickedButton = event.target as HTMLElement;
  if (clickedButton) {
    clickedButton.style.backgroundColor = '#00ff70';
  }
  
  const notImplementedText = document.createElement('p');
  notImplementedText.innerText = 'NOT IMPLEMENTED YET!';

  settingContent.appendChild(notImplementedText);
}

function cleanUpSettings() {
  const categoriesButtons = document.querySelectorAll('.ms-category-button');
  categoriesButtons.forEach(function (button) {
    if (button instanceof HTMLElement) {
      button.style.backgroundColor = '#e1e1e1';
    }
  });

  if (settingContent) {
    settingContent.innerHTML = '';
  }
}
