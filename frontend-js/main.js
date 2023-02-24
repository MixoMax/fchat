// Function to send a message to a chat
function sendMessage(sender, chat_id, message) {
    fetch('/send', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: `sender=${sender}&chat_id=${chat_id}&message=${message}`
    })
    .then(response => {
      console.log('Message sent:', response);
    })
    .catch(error => {
      console.error('Error sending message:', error);
    });
  }
  
  // Function to create a new chat
  function createChat(chat_id) {
    fetch('/new_chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: `chat_id=${chat_id}`
    })
    .then(response => {
      console.log('Chat created:', response);
    })
    .catch(error => {
      console.error('Error creating chat:', error);
    });
  }
  
  // Function to get messages from a chat
  function getMessages(chat_id) {
    fetch('/get', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: `chat_id=${chat_id}`
    })
    .then(response => response.json())
    .then(data => {
      console.log('Messages:', data);
    })
    .catch(error => {
      console.error('Error getting messages:', error);
    });
  }
  