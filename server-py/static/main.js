// Function to send a message to a chat
function sendMessage(chat_id, sender, message, password) {
	let time = Math.floor(Date.now() / 1000);

	let formData = new FormData();
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
  function createChat(new_chat_id, password) {
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
  function getMessages(chat_id, password) {
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
  function clearChat(chat_id, password) {
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

  function switch_chat(n) {
    switch (n) {
      case 1:
        chat_id = document.getElementById("chat_id").value;
        password = document.getElementById("password").value;
        break;
      case 2:
        chat_id = document.getElementById("new_chat_id").value;
        password = document.getElementById("new_chat_password").value;
        break;
      case 3:
        chat_id = document.getElementById("get_chat_id").value;
        password = document.getElementById("get_chat_password").value;
        break;
      case 4:
        chat_id = document.getElementById("clear_chat_id").value;
        password = document.getElementById("clear_chat_password").value;    
  }
  return chat_id, password;
  }

  function send() {
    switch_chat(1);
    let message = document.getElementById("message").value;
    let sender = localStorage.getItem("username");
    sendMessage(chat_id, sender, message, password);
  }

  function create() {
    switch_chat(2);
    createChat(chat_id, password);
  }

  function get() {
    switch_chat(3);
    getMessages(chat_id, password);
  }

  function clear() {
    switch_chat(4);
    clearChat(chat_id, password);
  }

  function login() {
    const sender = document.getElementById("username").value;
    console.log(sender);
    //save username in local storage
    localStorage.setItem("username", sender);
    //redirect to chat page
    window.location.replace("/chat");
  }