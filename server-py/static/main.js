// Function to send a message to a chat
function sendMessage() {
	let time = Math.floor(Date.now() / 1000);

	let formData = new FormData();
	let sender = document.getElementById("sender").value;
	let chat_id = document.getElementById("chat_id").value;
	let message = document.getElementById("message").value;
  let password = document.getElementById("password").value;
	formData.append('sender', sender);
	formData.append('chat_id', chat_id);
	formData.append('message', message);
	formData.append('timestamp', time);
  formData.append('password', password);
    fetch('/send', {
      method: 'POST',
      body: formData
    })
    .then(response => {
      console.log('Message sent:', response);
    })
    .catch(error => {
      console.error('Error sending message:', error);
    });
  }
  
  // Function to create a new chat
  function createChat() {
    let chat_id = document.getElementById("new_chat_id").value;
    let password = document.getElementById("new_chat_password").value;
    console.log(chat_id)
    let formData = new FormData();
    formData.append('chat_id', chat_id);
    formData.append('password', password);
    fetch('/new_chat', {
    	method: 'POST',
    	body: formData
    })
    .then(response => {
    	console.log('Chat created:', response);
    })
    .catch(error => {
    	console.error('Error creating chat:', error);
    });
  }
  
  // Function to get messages from a chat
  function getMessages() {
	let chat_id = document.getElementById("chat_id").value;
  let password = document.getElementById("get_chat_password").value;
	let formData = new FormData();
	formData.append('chat_id', chat_id);
  formData.append('password', password);
    fetch('/get', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      console.log('Messages:', data);
    })
    .catch(error => {
      console.error('Error getting messages:', error);
    });
  }
  
  //function to clear a chat
  function clearChat() {
    let chat_id = document.getElementById("clear_chat_id").value;
    let password = document.getElementById("clear_chat_password").value;
    let formData = new FormData();
    formData.append('chat_id', chat_id);
    formData.append('password', password);
    fetch('/clear', {
      method: 'POST',
      body: formData
    })
    .then(response => {
      console.log('Chat cleared:', response);
    })
    .catch(error => {
      console.error('Error clearing chat:', error);
    });
  }