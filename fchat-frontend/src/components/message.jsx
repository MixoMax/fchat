import "./message.css";

const Message = ({ message }) => {

    var message_is_mine = message.sender === 'Test User';

    return (
        <div className={`message-container vbox ${message_is_mine ? 'mine' : 'theirs'}`}>
            <div className="message-sender">{message.sender}</div>
            <div className="message-text">{message.text}</div>
        </div>
    );
}

export default Message;