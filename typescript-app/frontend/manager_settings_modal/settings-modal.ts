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
  managers_management_button.addEventListener(
    'click',
    DisplayManagerManagementSettings
  );
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
  managers_list.forEach((manager) => {
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
    photoObject.width = 100;
    photoObject.height = 100;

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

  const passwordChangeBlock = document.createElement('div') as HTMLDivElement;
  passwordChangeBlock.className = 'manager-change-password-container';

  const passwordChangeBlockName = document.createElement(
    'p'
  ) as HTMLParagraphElement;
  passwordChangeBlockName.innerText = 'Change password:';
  passwordChangeBlockName.className = 'manager-change-password-label';
  passwordChangeBlock.appendChild(passwordChangeBlockName);

  const oldPasswordInput = document.createElement('input') as HTMLInputElement;
  oldPasswordInput.type = 'password';
  oldPasswordInput.id = 'manager-change-password-old-password';
  oldPasswordInput.className = 'manager-change-password-old-password-input';
  oldPasswordInput.placeholder = 'Your old password';
  passwordChangeBlock.appendChild(oldPasswordInput);

  const newPasswordInput = document.createElement('input') as HTMLInputElement;
  newPasswordInput.type = 'password';
  newPasswordInput.id = 'manager-change-password-new-password';
  newPasswordInput.className = 'manager-change-password-new-password-input';
  newPasswordInput.placeholder = 'New password';
  passwordChangeBlock.appendChild(newPasswordInput);

  const newPasswordInput2 = document.createElement('input') as HTMLInputElement;
  newPasswordInput2.type = 'password';
  newPasswordInput2.id = 'manager-change-password-new2-password';
  newPasswordInput2.className = 'manager-change-password-new-password2-input';
  newPasswordInput2.placeholder = 'New password again';
  passwordChangeBlock.appendChild(newPasswordInput2);

  const newPasswordSubmitButton = document.createElement(
    'button'
  ) as HTMLButtonElement;
  newPasswordSubmitButton.innerText = 'Change';
  newPasswordSubmitButton.className = 'manager-change-password-submit-button';
  passwordChangeBlock.appendChild(newPasswordSubmitButton);

  newPasswordSubmitButton.addEventListener('click', passwordChangeButtonClick);
  settingContent.appendChild(passwordChangeBlock);
}

function passwordChangeButtonClick() {
  const old_password = document.getElementById(
    'manager-change-password-old-password'
  ) as HTMLInputElement;
  const new_password = document.getElementById(
    'manager-change-password-new-password'
  ) as HTMLInputElement;
  const new_password2 = document.getElementById(
    'manager-change-password-new2-password'
  ) as HTMLInputElement;

  if (old_password.value.length == 0) {
    alert('Please enter old password!');
  } else if (new_password.value !== new_password2.value) {
    alert('New passwords does not match, please double check!');
  } else if (new_password.value.length < 6) {
    alert('New password should include at least 6 symbols!');
  } else {
    // TODO CALL API HERE AND CHANGE PASSWORD
    alert('Password changing are not implemented yet!');
  }
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
