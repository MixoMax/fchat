import {useEffect, useState} from 'react';
import Message from './message';
import "./chat.css";

const Chat = ({ chat_id }) => {
    const [chat, setChat] = useState(null);
    
    useEffect(() => {
        //manual override
        var data = {
            "name": "Test Chat",
            "messages": [
                {
                    "sender": "Test User",
                    "text": "Hello World!"
                },
                {
                    "sender": "Test User",
                    "text": "This is a test message."
                },
                {
                    "sender": "MixoMax",
                    "text": "This is a test response."
                }
            ]
        };
        setChat(data);
    }, [chat_id]);
    
    return (
        <div className="chat vbox">
            <h1 className="chat-header">{chat ? chat.name : 'Loading...'}</h1>
            
            <div className="messages-box vbox">
                {chat ? chat.messages.map((message, index) => (
                    <Message key={index} message={message} />
                )) : 'Loading...'}
            </div>
            <div className="chat-input hbox">
                <input type="text" placeholder="Type a message..." />
                <button
                    onClick={() => {
                        var message = document.querySelector('.chat-input input').value;
                        setChat({
                            ...chat,
                            messages: chat.messages.concat({
                                sender: 'Test User',
                                text: message
                            })
                        });
                    }}
                > Send </button>
            </div>
        </div>
    );
}

export default Chat;