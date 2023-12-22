import io from 'socket.io-client';

let active_chat = 0;

interface ChatListItem {
  user_id: string;
  last_message_text: string;
  unread_count: number;
  last_message_time: string;
  photo_uuid: string;
  username: string;
  name: string;
}

interface ChatListContainer {
  chat_list: ChatListItem[];
}

interface Message {
  message_text: string | null;
  date: string;
  chat_id: number;
  from_user: number;
  unread: boolean | null;
  attachment: MessageAttachment | null;
  location: MessageLocation | null;
  manager_name: string | null;
  reply_to_message: Message | null;
}

interface MessageAttachment {
  file_id: string;
  mime_type: string;
  file_name: string;
}

interface MessageLocation {
  latitude: number;
  longitude: number;
}

interface MessageList {
  messages_list: Message[];
}

const socket = io();
socket.on('new_message', function (message: Message) {
  if (message.hasOwnProperty('manager_name')) {
    var audio = new Audio('mixkit-message-pop-alert-2354.mp3');
    audio.play();
  } else {
    var audio = new Audio('mixkit-correct-answer-tone-2870.wav');
    audio.play();
  }
  if (String(active_chat) === String(message['chat_id'])) {
    markChatAsRead(active_chat);
    DisplayMessage(message);
  }
  getChatListFromApi();
});

document.addEventListener('DOMContentLoaded', function () {
  getChatListFromApi();
  let message_send_button = document.getElementById(
    'message-send-button'
  ) as HTMLButtonElement;
  message_send_button.addEventListener('click', sendMessageToCustomer);
  let add_attachment_button = document.getElementById(
    'attachment-send-button'
  ) as HTMLButtonElement;
  add_attachment_button.addEventListener('click', FileUpload);

  let message_input = document.getElementById(
    'message-input'
  ) as HTMLTextAreaElement;
  message_input.addEventListener('keyup', function (event) {
    event.preventDefault();
    if (event.key === 'Enter') {
      sendMessageToCustomer();
    }
  });
});

function FileUpload() {
  let attachment_input = document.getElementById(
    'file-input'
  ) as HTMLInputElement;

  attachment_input.click();
  attachment_input.addEventListener('change', function (event) {
    const input = event.target as HTMLInputElement;

    if (input && input.files && input.files.length > 0) {
      const file = input.files[0];
      if (file) {
        // Read the file as a binary blob
        const reader = new FileReader();
        reader.onload = function (evt) {
          const fileReader = evt.target as FileReader;
          if (fileReader && fileReader.result) {
            const fileReader = evt.target as FileReader;
            const binary = fileReader.result;
            let headers = {
              'X-Filename': file.name,
              'Content-Type': file.type
            };

            fetch('/tg-bot/file_upload', {
              method: 'POST',
              body: binary,
              headers: headers
            })
              .then((response) => response.json())
              .then((data) => {
                if (
                  (data.error && data.error === 'file uploaded!') ||
                  data.error === 'file already exists!'
                ) {
                  const fileList = document.getElementById(
                    'files-attachment-list'
                  );
                  if (fileList) {
                    fileList.innerHTML = '';
                  }
                  const listItem = document.createElement('li');
                  listItem.classList.add('file-attached');
                  listItem.id = data['file_id'];
                  const fileName = document.createElement('p');
                  fileName.classList.add('attached-file-name');
                  fileName.id = 'attached-file-name';
                  fileName.innerText = file.name;
                  listItem.appendChild(fileName);
                  const removeButton = document.createElement('button');
                  removeButton.classList.add('remove-attachment-button');
                  removeButton.innerText = 'Remove';
                  removeButton.onclick = function () {
                    listItem.remove();
                  };

                  listItem.appendChild(removeButton);
                  if (fileList) {
                    fileList.appendChild(listItem);
                  }
                  console.log('File uploaded id:', data['file_id']);
                } else {
                  alert(`Error: ${data.error}`);
                  console.error('Failed to upload file:', data.error);
                }
              })
              .catch((error) => {
                console.error(
                  'There has been a problem with your fetch operation:',
                  error
                );
              });
          }
          reader.readAsArrayBuffer(file);
        };
      }
    }
  });
}

const acceptedPhotoExtensions = [
  '.jpg',
  '.jpeg',
  '.png',
  '.gif',
  '.bmp',
  '.tiff'
];
const acceptedAudioExtensions = ['.MP3', '.M4A'];
const acceptedVideoExtensions = ['.MPEG4'];

function sendMessageToCustomer() {
  let file_attachment_id: string | null = null;
  let file_attachment_name: string | null = null;

  const fileList = document.getElementById('files-attachment-list');
  if (fileList) {
    const fileAttachedList = fileList.querySelectorAll('li');
    fileAttachedList.forEach((fileAttached) => {
      file_attachment_id = fileAttached.id;
      const fileNameElement = document.getElementById('attached-file-name');
      if (fileNameElement) {
        file_attachment_name = fileNameElement.innerText;
      }
    });
  }

  console.log('file_attachment_id', file_attachment_id);
  console.log('file_attachment_name', file_attachment_name);

  let message_text_input = document.getElementById(
    'message-input'
  ) as HTMLInputElement;
  let message_text = message_text_input.value;
  const payload = {
    chat_id: active_chat,
    text: message_text,
    file_attachment_id: file_attachment_id
  };
  let target_api_method: string = 'new-text-message';

  if (file_attachment_name) {
    const lowerCaseName = (file_attachment_name as string).toLowerCase();

    if (acceptedPhotoExtensions.some((ext) => lowerCaseName.endsWith(ext))) {
      target_api_method = 'new-photo-message';
    } else if (
      acceptedAudioExtensions.some((ext) => lowerCaseName.endsWith(ext))
    ) {
      target_api_method = 'new-audio-message';
    } else if (
      acceptedVideoExtensions.some((ext) => lowerCaseName.endsWith(ext))
    ) {
      target_api_method = 'new-video-message';
    } else {
      target_api_method = 'new-document-message';
    }
  }

  var authToken = getCookie('AUTHToken');
  fetch(`/tg-bot/` + target_api_method, {
    method: 'POST', // Set the method to POST
    headers: {
      'Content-Type': 'application/json',
      AuthorizationToken: authToken
    },
    body: JSON.stringify(payload) // Stringify your payload and set it in the body property
  }).then((response) => {
    if (response.status === 200) {
      return response.json().then((data) => {
        if (fileList) {
          fileList.innerHTML = '';
        }
        message_text_input.value = '';
        console.log('Success message was sent', data);
      });
    } else {
      return response.json().then((data) => {
        alert(`Error: ${data['result']}`);
        console.error('Error:', data['result']);
      });
    }
  });
}

function loadChatMessages(chat_id: number) {
  fetch('/tg-bot/get-messages/' + chat_id, {
    method: 'GET'
  })
    .then((response) => {
      if (response.status !== 200) {
        throw new Error('Network response was not ok ' + response.statusText);
      }
      return response.json(); // Parse JSON response
    })
    .then((data) => {
      console.log('Data received:', data);
      displayChatHistory(data); // Function to handle the display of data
    })
    .catch((error) => {
      console.error(
        'There has been a problem with your fetch operation:',
        error
      );
    });
}

function displayChatHistory(message_list: MessageList) {
  const messagesList = document.getElementById('messages-list');
  if (messagesList) {
    messagesList.innerHTML = '';
  }
  message_list.messages_list.forEach((message_from_db: Message) => {
    DisplayMessage(message_from_db);
  });
}

function DisplayMessage(message_object: Message) {
  const messagesList = document.getElementById(
    'messages-list'
  ) as HTMLUListElement;
  const messageElement: HTMLLIElement = document.createElement('li');
  if (String(message_object.from_user) === String(active_chat)) {
    messageElement.className = 'message-from-client';
  } else {
    messageElement.className = 'message-from-manager';
  }
  if (message_object.attachment && message_object.attachment.mime_type) {
    const attachment_source =
      '/tg-bot/file?file_uuid=' + message_object.attachment.file_id;
    if (message_object.attachment.mime_type.startsWith('image/')) {
      const photoObject = document.createElement('img');
      const photoObjectUrl = document.createElement('a');
      photoObjectUrl.href = attachment_source;
      photoObject.classList.add('message-image');
      photoObject.src = attachment_source;
      photoObject.width = 200;
      photoObject.height = 300;
      photoObjectUrl.appendChild(photoObject);
      messageElement.appendChild(photoObjectUrl);
    } else if (message_object.attachment.mime_type.startsWith('video/')) {
      const videoObject = document.createElement('video');
      videoObject.classList.add('message-video');
      videoObject.src = attachment_source;
      videoObject.width = 400;
      videoObject.height = 300;
      videoObject.controls = true;
      messageElement.appendChild(videoObject);
    } else if (message_object.attachment.mime_type.startsWith('audio/')) {
      const audioObject = document.createElement('audio');
      audioObject.classList.add('message-audio');
      audioObject.src = attachment_source;
      audioObject.controls = true;
      messageElement.appendChild(audioObject);
    } else if (message_object.attachment.mime_type.startsWith('application/')) {
      const fileExtension =
        message_object.attachment.file_name.split('.').pop() || 'file';

      const fileIcon = document.createElement('span');
      fileIcon.classList.add('message-application-icon');
      fileIcon.innerText = `${fileExtension.toUpperCase()} File`;
      messageElement.appendChild(fileIcon);

      const EmptyNewLine = document.createElement('p');
      const downloadLink = document.createElement('a');
      EmptyNewLine.classList.add('message-application-empty-line');
      downloadLink.classList.add('message-download-link');
      downloadLink.href = attachment_source;
      downloadLink.innerText = `${message_object.attachment.file_name}`;
      downloadLink.download = message_object.attachment.file_name;
      messageElement.appendChild(EmptyNewLine);
      messageElement.appendChild(downloadLink);
    }
  }

  if (message_object.location) {
    var url =
      'https://www.google.com/maps?q=' +
      message_object.location.latitude +
      ',' +
      message_object.location.longitude;
    var embedUrl =
      'https://www.google.com/maps/embed?pb=!1m14!1m12!1m3!1d12090.442629191114!2d' +
      message_object.location.longitude +
      '!3d' +
      message_object.location.latitude +
      '!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!5e0!3m2!1sen!2s!4v1651254363314!5m2!1sen!2s';
    const mapLinkeble = document.createElement('a');
    mapLinkeble.href = url;
    const mapIframe = document.createElement('iframe');
    mapIframe.id = 'mapPreview';
    mapIframe.classList.add('map-preview');
    mapIframe.src = embedUrl;
    mapLinkeble.appendChild(mapIframe);
    messageElement.appendChild(mapLinkeble);

    const locationCoordinatesText = document.createElement('p');
    locationCoordinatesText.classList.add('location-coordinates');
    locationCoordinatesText.innerText =
      message_object.location.latitude +
      ',' +
      message_object.location.longitude;
    messageElement.appendChild(locationCoordinatesText);
  }

  if (message_object.manager_name) {
    const messageAutor = document.createElement('p');
    messageAutor.classList.add('message-manager-name');
    messageAutor.innerText = message_object.manager_name;
    messageElement.appendChild(messageAutor);
  }

  if (message_object.message_text) {
    const messageText = document.createElement('p');
    messageText.classList.add('message-text');
    messageText.innerText = message_object.message_text;
    messageElement.appendChild(messageText);
  }

  const messageDate = document.createElement('p');
  messageDate.classList.add('message-date');
  messageDate.innerText = message_object.date;
  messageElement.appendChild(messageDate);

  messagesList.appendChild(messageElement);
  messageElement.scrollIntoView({ behavior: 'smooth' });
}

function getCookie(name: string) {
  var cookieArr = document.cookie.split(';');
  for (var i = 0; i < cookieArr.length; i++) {
    var cookiePair = cookieArr[i].split('=');
    if (name == cookiePair[0].trim()) {
      return decodeURIComponent(cookiePair[1]);
    }
  }
  return '';
}

function getChatListFromApi() {
  fetch('/tg-bot/chat-list', {
    method: 'GET'
  })
    .then((response) => {
      if (response.status !== 200) {
        throw new Error('Network response was not ok ' + response.statusText);
      }
      return response.json();
    })
    .then((data) => {
      console.log('Data received:', data);
      displayDialogList(data);
    })
    .catch((error) => {
      console.error(
        'There has been a problem with your fetch operation:',
        error
      );
    });
}

function markChatAsRead(chat_id: number) {
  const payload = { chat_id: chat_id };
  fetch(`/tg-bot/mark-chat-as-read`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  }).then((response) => {
    if (response.status === 200) {
      return response.json().then((data) => {
        console.log('Mark as read', data);
      });
    } else {
      return response.json().then((data) => {
        alert(`Error: ${data['result']}`);
        console.error('Error:', data['result']);
      });
    }
  });
}

function displayDialogList(chat_list: ChatListContainer) {
  const contactList = document.getElementById('contacts');
  if (contactList) {
    contactList.innerHTML = '';
  }

  chat_list.chat_list.forEach((chatItem: ChatListItem) => {
    const ContactItem = document.createElement('li');
    ContactItem.id = `contact-item-object_${chatItem.user_id}`;
    ContactItem.className = 'contact-item';

    if (String(active_chat) === String(chatItem.user_id)) {
      ContactItem.classList.add('active-contact');
    }

    const chatPhotoContainer = document.createElement('div');
    chatPhotoContainer.classList.add('chat-photo-container');

    if (chatItem.hasOwnProperty('photo_uuid')) {
      const attachment_source = '/tg-bot/file?file_uuid=' + chatItem.photo_uuid;
      const photoObject = document.createElement('img');
      photoObject.classList.add('chat-photo');
      photoObject.src = attachment_source;
      photoObject.width = 50;
      photoObject.height = 50;
      chatPhotoContainer.appendChild(photoObject);
    } else {
      const attachment_source = 'user_empty_photo.png';
      const photoObject = document.createElement('img');
      photoObject.classList.add('chat-photo');
      photoObject.src = attachment_source;
      photoObject.width = 50;
      photoObject.height = 50;
      chatPhotoContainer.appendChild(photoObject);
    }

    ContactItem.appendChild(chatPhotoContainer);

    const nameAndDateAndLastMessageDiv = document.createElement('div');
    nameAndDateAndLastMessageDiv.classList.add('name-date-message-container');

    const nameParagraph = document.createElement('p');
    nameParagraph.classList.add('chat-name');
    nameParagraph.textContent = chatItem.name;
    nameAndDateAndLastMessageDiv.appendChild(nameParagraph);

    const timeParagraph = document.createElement('p');
    timeParagraph.classList.add('chat-last-message-date');
    timeParagraph.textContent = chatItem.last_message_time;
    nameAndDateAndLastMessageDiv.appendChild(timeParagraph);

    const messageParagraph = document.createElement('p');
    messageParagraph.classList.add('chat-last-message');
    messageParagraph.textContent = chatItem.last_message_text;

    nameAndDateAndLastMessageDiv.appendChild(messageParagraph);
    ContactItem.appendChild(nameAndDateAndLastMessageDiv);

    if (Number(active_chat) !== Number(chatItem.user_id)) {
      if (Number(chatItem.unread_count) !== 0) {
        const unreadMessagesContainer = document.createElement('div');
        unreadMessagesContainer.classList.add('unread-messages-container');
        unreadMessagesContainer.id = `unread-message-container_${chatItem.user_id}`;
        const UnreadMessagesCount = document.createElement('p');
        UnreadMessagesCount.classList.add('chat-unread-messages');
        UnreadMessagesCount.textContent = chatItem.unread_count.toString();
        unreadMessagesContainer.appendChild(UnreadMessagesCount);
        ContactItem.appendChild(unreadMessagesContainer);
      }
    }

    if (contactList) {
      contactList.appendChild(ContactItem);
    }
  });

  let contactListItems = document.querySelectorAll('#contacts li');

  contactListItems.forEach((li) => {
    li.addEventListener('click', (event) => {
      const chatSettingImage = document.getElementById('chat-setting-image');
      const chatSettingFullName = document.getElementById(
        'chat-setting-full-name'
      );

      let uniqueNumber = Number(
        (event.currentTarget as HTMLElement).id.split('_')[1]
      );

      if (Number(active_chat) !== Number(uniqueNumber)) {
        contactListItems.forEach((item) => {
          item.classList.remove('active-contact');
        });

        console.log('Unique chat ID:', uniqueNumber);
        loadChatMessages(uniqueNumber);
        console.log('Messages loaded!', uniqueNumber);
        markChatAsRead(uniqueNumber);
        console.log('Chats updated!', uniqueNumber);
        (event.currentTarget as HTMLElement).classList.add('active-contact');

        var unreadMessagesContainer = document.getElementById(
          `unread-message-container_${uniqueNumber}`
        );
        if (unreadMessagesContainer) {
          unreadMessagesContainer.style.display = 'none';
        } else {
          console.log('Element not found');
        }

        let chatNameElement = (
          event.currentTarget as HTMLElement
        ).querySelector('.chat-name');
        let chatName = chatNameElement
          ? chatNameElement.textContent
          : 'Default Name';

        let chatPhotoElement = (
          event.currentTarget as HTMLElement
        ).querySelector('.chat-photo') as HTMLImageElement;
        let chatPhotoSrc =
          '/tg-bot/file?file_uuid=' + chatPhotoElement
            ? chatPhotoElement.src
            : '/user_empty_photo.png';

        if (chatSettingFullName) {
          chatSettingFullName.textContent = chatName;
        }
        if (chatPhotoElement) {
          chatPhotoElement.src = chatPhotoSrc;
        }

        var chatSettingTopPanel = document.getElementById(
          `top_chat_setting_panel`
        );
        if (chatSettingTopPanel) {
          chatSettingTopPanel.style.display = 'flex';
        } else {
          console.log('Element chatSettingTopPanel not found');
        }

        var inputPanel = document.getElementById(
          'input_chat_box'
        ) as HTMLDivElement;
        inputPanel.style.display = 'flex';
        active_chat = uniqueNumber;
      }
    });
  });
}
console.log('active_chat', active_chat);
