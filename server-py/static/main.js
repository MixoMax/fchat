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
      localStorage.setItem("chat_id", chat_id);
      localStorage.setItem("password", password);

      change_chat();
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
    .then(response => {
      console.log(response)
      if(response.status == 200) {
        return response.json().then(data => {	
          return data;
        });
      } else {
        return response.status;
      }
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
    if(document.getElementById("message_input").placeholder == "Join a chat to send messages") return no_chat();
    let message_input = document.getElementById("message_input");
    let message = message_input.value;
    message_input.value = "";
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

  // Function is never called
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
    if(chat_id == "" || password == "") return;

    

    localStorage.setItem("chat_id", chat_id);
    localStorage.setItem("password", password);

    console.log(chat_id, password)
      
    //print message_list to div id="message_list"
    if(!update_chat()){
      return
    }else{
      document.getElementById("chat_id").value = "";
      document.getElementById("chat_password").value = "";
      document.getElementById("chat_name").innerHTML = "";
      document.getElementById("message_input").placeholder = "Send a message in " + chat_id;
    }
  }
  
  async function update_chat() {
    try {
      let chat_id = localStorage.getItem("chat_id");
      let password = localStorage.getItem("password");
      let user = localStorage.getItem("username");
      let message_list = await getMessages(chat_id, password);
      if(message_list != 401 && message_list != 404){
        let message_list_html = "";
        for (let i = 0; i < message_list.length; i++) {  m
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
        const message_list_div = document.getElementById("message_list");
        message_list_div.innerHTML = message_list_html;
        message_list_div.scrollTop = message_list_div.scrollHeight - message_list_div.clientHeight;
        return true;
      }else return false;
    } catch (error) {
      console.error('Error:', error);
    }
  }

// 
function change_password_visibility(){
  const password_visibility_button = document.getElementById("password_visibility_button"); 
  const password_field = document.getElementById("chat_password");
  if (password_visibility_button.value == "true") {
    password_field.type = "password";
    password_visibility_button.value = "false";
    password_visibility_button.innerHTML = "Show Password";
  } else {
    password_field.type = "text";
    password_visibility_button.value = "true";
    password_visibility_button.innerHTML = "Hide Password";
  }
}

function send_message_on_enter(event) {
  if (event.keyCode == 13) {
    send();
  }
}

function change_chat_on_enter(event) {
  if (event.keyCode == 13) {
    change_chat();
  }
}

function no_chat(){
  document.getElementById("no_chat").style.top = "790px";
  setTimeout(()=>{
    document.getElementById("no_chat").style.top = "830px";
  }, 2500) 
}