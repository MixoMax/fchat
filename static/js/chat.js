//apis:
//"/api/get_chat/<chat_id>"
//"/api/create_chat/<chat_name>/<chat_password>"
//"/api/send_message" (POST) {"chat_id", "sender", "content", "response_to"}

const chat_div = document.getElementById("chat_div")

function get_chat(chat_id) {
    //get json object from request
    
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
        let html_string = `<div class="Message"><p id="sender">` + this.sender + `<\p><p id="timestamp">` + this.timestamp + `<\p><p id="content">` + this.content + `<\p>`
        if (this.response_to != null) {
            html_string += `<p id="response_to">` + this.response_to + `<\p>`
        }
        html_string += `</div>`
        chat_div.innerHTML += html_string
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

function create_chat(chat_name, chat_password) {
    //make get request to "/api/create_chat/<chat_name>/<chat_password>"

    fetch("/api/create_chat/" + chat_name + "/" + chat_password).then(response => {
        console.log(response.status)
    })
}

function send_message(chat_id, sender, content, response_to = null) {
    //make post request to /api/send_message

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