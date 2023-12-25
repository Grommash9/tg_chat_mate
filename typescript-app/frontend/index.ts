import io from 'socket.io-client';
import FileUpload from './api_methods/file_upload.js';
import getChatListFromApi from './api_methods/get_chat_list.js';
import markChatAsRead from './api_methods/mark_chat_as_read.js';
import loadChatMessages from './api_methods/get_chat_messages.js';
import SendMessage from './api_methods/send_message.js';

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
    var audio = new Audio('/files/mixkit-message-pop-alert-2354.mp3');
    audio.play();
  } else {
    var audio = new Audio('/files/mixkit-correct-answer-tone-2870.wav');
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

  SendMessage(target_api_method, payload).then((result) => {
    if (result) {
      if (fileList) {
        fileList.innerHTML = '';
      }
      message_text_input.value = '';
    } else {
      // There was an error sending the message
    }
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
  var messageElement = CreateMessageHTMLObject(message_object);
  messagesList.appendChild(messageElement);
  messageElement.scrollIntoView({ behavior: 'smooth' });
}

function getHTMLLocation(location: MessageLocation): HTMLAnchorElement {
  var url =
    'https://www.google.com/maps?q=' +
    location.latitude +
    ',' +
    location.longitude;
  var embedUrl =
    'https://www.google.com/maps/embed?pb=!1m14!1m12!1m3!1d12090.442629191114!2d' +
    location.longitude +
    '!3d' +
    location.latitude +
    '!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!5e0!3m2!1sen!2s!4v1651254363314!5m2!1sen!2s';
  const mapLinkeble = document.createElement('a');
  mapLinkeble.href = url;
  const mapIframe = document.createElement('iframe');
  mapIframe.id = 'mapPreview';
  mapIframe.classList.add('map-preview');
  mapIframe.src = embedUrl;
  mapLinkeble.appendChild(mapIframe);
  return mapLinkeble;
}

function getAttachmentHTMLCode(attachment: MessageAttachment) {
  const attachment_source = '/tg-bot/file?file_uuid=' + attachment.file_id;
  if (attachment.mime_type.startsWith('image/')) {
    const photoObject = document.createElement('img');
    const photoObjectUrl = document.createElement('a');
    photoObjectUrl.href = attachment_source;
    photoObject.classList.add('message-image');
    photoObject.src = attachment_source;
    photoObject.width = 200;
    photoObject.height = 300;
    photoObjectUrl.appendChild(photoObject);
    return photoObjectUrl;
  } else if (attachment.mime_type.startsWith('video/')) {
    const videoObject = document.createElement('video');
    videoObject.classList.add('message-video');
    videoObject.src = attachment_source;
    videoObject.width = 400;
    videoObject.height = 300;
    videoObject.controls = true;
    return videoObject;
  } else if (attachment.mime_type.startsWith('audio/')) {
    const audioObject = document.createElement('audio');
    audioObject.classList.add('message-audio');
    audioObject.src = attachment_source;
    audioObject.controls = true;
    return audioObject;
  } else {
    const fileObject = document.createElement('div');
    const fileExtension = attachment.file_name.split('.').pop() || 'file';

    const fileIcon = document.createElement('span');
    fileIcon.classList.add('message-application-icon');
    fileIcon.innerText = `${fileExtension.toUpperCase()} File`;
    fileObject.appendChild(fileIcon);

    const EmptyNewLine = document.createElement('p');
    const downloadLink = document.createElement('a');
    EmptyNewLine.classList.add('message-application-empty-line');
    downloadLink.classList.add('message-download-link');
    downloadLink.href = attachment_source;
    downloadLink.innerText = `${attachment.file_name}`;
    downloadLink.download = attachment.file_name;
    fileObject.appendChild(EmptyNewLine);
    fileObject.appendChild(downloadLink);

    return fileObject;
  }
}

function CreateMessageHTMLObject(message_object: Message): HTMLLIElement {
  const messageElement: HTMLLIElement = document.createElement('li');
  if (String(message_object.from_user) === String(active_chat)) {
    messageElement.className = 'message-from-client';
  } else {
    messageElement.className = 'message-from-manager';
  }

  if (message_object.reply_to_message) {
    var r_message_object = message_object.reply_to_message;

    var replyMessageObject = document.createElement('div');
    replyMessageObject.className = 'reply-to-message';

    if (r_message_object.attachment && r_message_object.attachment.mime_type) {
      var attachmentHTML = getAttachmentHTMLCode(r_message_object.attachment);
      replyMessageObject.appendChild(attachmentHTML);
    }

    if (r_message_object.location) {
      var locationHTMLBlock = getHTMLLocation(r_message_object.location);
      replyMessageObject.appendChild(locationHTMLBlock);
    }

    if (r_message_object.manager_name) {
      const messageAutor = document.createElement('p');
      messageAutor.classList.add('message-manager-name');
      messageAutor.innerText = r_message_object.manager_name;
      replyMessageObject.appendChild(messageAutor);
    }

    if (r_message_object.message_text) {
      const messageText = document.createElement('p');
      messageText.classList.add('message-text');
      messageText.innerText = r_message_object.message_text;
      replyMessageObject.appendChild(messageText);
    }

    const messageDate = document.createElement('p');
    messageDate.classList.add('message-date');
    messageDate.innerText = r_message_object.date;
    replyMessageObject.appendChild(messageDate);

    messageElement.appendChild(replyMessageObject);
  }

  if (message_object.attachment && message_object.attachment.mime_type) {
    var attachmentHTML = getAttachmentHTMLCode(message_object.attachment);
    messageElement.appendChild(attachmentHTML);
  }

  if (message_object.location) {
    var locationHTMLBlock = getHTMLLocation(message_object.location);
    messageElement.appendChild(locationHTMLBlock);
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

  return messageElement;
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
      const chatSettingImage = document.getElementById(
        'chat-setting-image'
      ) as HTMLImageElement;
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
            : '/files/user_empty_photo.png';

        if (chatSettingFullName) {
          chatSettingFullName.textContent = chatName;
        }
        if (chatSettingImage) {
          chatSettingImage.src = chatPhotoSrc;
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

export { displayDialogList, displayChatHistory };
