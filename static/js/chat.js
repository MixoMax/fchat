//apis:
//"/api/get_chat/<chat_id>"
//"/api/create_chat/<chat_name>/<chat_password>"
//"/api/send_message" (POST) {"chat_id", "sender", "content", "response_to"}

const chat = document.getElementById('chat_id')

console.log("chat.js loaded")

function get_chat() {
    //get json object from request

    const chat_id = document.getElementById('chat_id').value
    
    fetch("/api/get_chat/" + chat_id).then(async response => {
        let chat_array = await response.json()
        console.log(chat_array)
        update_chat(chat_array) //chat_array cant be a promise but is
    })
}

class Message {
    //store a message as an object
    constructor(message_id, sender, content, timestamp, response_to) {
        this.message_id = message_id
        this.sender = sender
        this.content = content
        this.timestamp = timestamp
        this.response_to = response_to
    }
    append_to_div() {
        const chat_div = document.getElementById("chat_div")
        const date = new Date(this.timestamp * 1000)
        this.timestamp = date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds()


        let html_string = `<div class="incoming_message" id="${"message" + this.message_id}"><p class="message_sender">${this.sender}<\p><p class="message_timestamp">${this.timestamp}<\p><p class="message_content">${this.content}<\p>`
        if (this.response_to != null) {
            html_string += `<p id="response_to">` + this.response_to + `<\p>`
        }
        html_string += `</div>`
        chat_div.innerHTML += html_string

        let messageDiv = document.getElementById("message" + this.message_id)
        let senderElement = messageDiv.querySelector(".message_sender")
        let contentElement = messageDiv.querySelector(".message_content")
        console.log(contentElement.style.fontFamily)
        //make the width of the message fit the text or sender depending on whats longer but also maxiamal 80%
        let message_width = Math.max(senderElement.textContent.length, senderElement.textContent.length)
        console.log("1", senderElement.textContent.length, "2", contentElement.textContent.length, "3", message_width, "4", window.innerWidth)
        messageDiv.style.width = Math.min(message_width * 20 + 20, 0.64 * window.innerWidth) + "px"
        
        
        messageDiv.style.height = "auto"
    }
    toString() {
        let str = `Message: (id: ${this.message_id}, sender: ${this.message_id}, content: ${this.content}, timestamp: ${this.timestamp})`
    }

}

function update_chat(chat_array) {
    console.log("update")
    chat_array.forEach(element => {
        let message = new Message(element.message_id, element.sender, element.content, element.timestamp, element.response_to)
        message.append_to_div()
        console.log(message.toString())
    });
    console.log("done")
}

function create_chat() {

    const chat_name = document.getElementById("chat_name").value
    const chat_password = document.getElementById("chat_password").value

    if(chat_name == "" || chat_password == "") {
        alert("Please enter a chat name and password")
        return
    }

    fetch("/api/create_chat/" + chat_name + "/" + chat_password).then(response => {
        console.log(response.status)
    })
}

function send_message() {

    const chat_id = document.getElementById('chat_id').value
    const sender = document.getElementById('sender').value
    const content = document.getElementById('content').value
    const response_to = document.getElementById('response_to').value || null

    if(chat_id == "" || sender == "" || content == "") {
        alert("Please enter a chat id, sender, and content")
        return
    }


    let payload = {"chat_id": chat_id, "sender": sender, "content": content, "response_to": response_to}
    fetch("/api/send_message", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        charset: "utf-8",
        body: JSON.stringify(payload)
    }).then(response => {
        console.log(response.status)
    })
}