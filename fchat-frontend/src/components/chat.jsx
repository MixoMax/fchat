import {useEffect, useState} from 'react';
import Message from './message';
import "./chat.css";

const Chat = ({ chat_id, setChat, chat_messages, setChatMessages, user }) => {
    const [chat_name, setChatName] = useState(null);

    useEffect(() => {
        if (chat_id) {
            setChatName("Example Chat");
        }
    }, [chat_id]);

    
    return (
        <div className="chat vbox">
            <h1 className="chat-header">{chat_name}</h1>
            
            <div className="messages-box vbox">
                {chat_messages.map((message, index) => {
                    //set message.is_mine to true if the message sender is the current user
                    message.is_mine = message.sender === user;
                    return <Message key={index} message={message} />
                })}
            </div>
            <div className="chat-input hbox">
                <input type="text" placeholder="Type a message..." onKeyPress={(e) => {
                    if (e.key === "Enter") {
                        var message_input = document.querySelector('.chat-input input');
                        var message_content = message_input.value;
                        if (message_content && user) {
                            var new_message = {
                                sender: user,
                                text: message_content
                            };
                            setChatMessages([...chat_messages, new_message]);
                        }
                        message_input.value = "";
                    }
                }} />

                <button
                    onClick={() => {
                        var message_input = document.querySelector('.chat-input input');
                        var message_content = message_input.value;
                        if (message_content && user) {
                            var new_message = {
                                sender: user,
                                text: message_content
                            };
                            setChatMessages([...chat_messages, new_message]);
                        }
                        message_input.value = "";
                    }}
                > Send </button>
            </div>
        </div>
    );
}

export default Chat;