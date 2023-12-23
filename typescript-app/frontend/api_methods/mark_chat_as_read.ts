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

export default markChatAsRead;