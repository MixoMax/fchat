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
    return fetch('/get', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      console.log('Messages:', data);
      return data;
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



  function send() {
    let message = document.getElementById("message").value;
    chat_id = localStorage.getItem("chat_id");
    password = localStorage.getItem("password");
    let sender = localStorage.getItem("username");
    sendMessage(chat_id, sender, message, password);
    update_chat();
  }

  function create() {
    try {
      chat_id = document.getElementById("chat_id").value;
      password = document.getElementById("chat_password").value;
    } catch (error) {
    chat_id = localStorage.getItem("chat_id");
    password = localStorage.getItem("password");
    }
    createChat(chat_id, password);
  }

  function get() {
    chat_id = localStorage.getItem("chat_id");
    password = localStorage.getItem("password");
    getMessages(chat_id, password);
  }

  function clear_current_chat() {
    console.log("clear")
    try {
      chat_id = document.getElementById("chat_id").value;
      password = document.getElementById("chat_password").value;
    } catch (error) {
      console.log(error)
    chat_id = localStorage.getItem("chat_id");
    password = localStorage.getItem("password");
    }
    console.log(chat_id, password)
    clearChat(chat_id, password);
  }

  function login() {
    const sender = document.getElementById("username").value;
    //save username in local storage
    localStorage.setItem("username", sender);
    //redirect to chat page
    window.location.replace("/chat");
  }

  async function change_chat() {
    let chat_id = document.getElementById("chat_id").value;
    let password = document.getElementById("chat_password").value;
      
    localStorage.setItem("chat_id", chat_id);
    localStorage.setItem("password", password);

    console.log(chat_id, password)
      
    //print message_list to div id="message_list"
    update_chat();
    
  }
  
  async function update_chat() {
    try {
      let chat_id = localStorage.getItem("chat_id");
      let password = localStorage.getItem("password");
      let user = localStorage.getItem("username");
      let message_list = await getMessages(chat_id, password);
      let message_list_html = "";
      for (let i = 0; i < message_list.length; i++) {
        let message = message_list[i];
        let time_delta = Math.floor(Date.now() / 1000) - message[2];
        let time_string = "";
        if (time_delta < 60) {
          time_string = time_delta + "s";
        } else if (time_delta < 3600) {
          time_string = Math.floor(time_delta / 60) + "m";
        } else if (time_delta < 86400) {
          time_string = Math.floor(time_delta / 3600) + "h";
        } else {
          time_string = Math.floor(time_delta / 86400) + "d";
        }
        message[2] = time_string;
        if (message[0] == user) {
          message[0] = "You";
        }
        if (message[0] == "You") {
          message_html = `
          <div class="message">
            <div class="user_sender">${message[0]}, ${message[2]}</div>
            <div class="user_text">${message[1]}</div>
          </div>`
        } else {
          
        message_html = `
          <div class="message">
            <div class="sender">${message[0]}, ${message[2]}</div>
            <div class="text">${message[1]}</div>
          </div>
        `;}
        message_list_html += message_html;
      }
      document.getElementById("message_list").innerHTML = message_list_html;
    } catch (error) {
      console.error('Error:', error);
    }
  }