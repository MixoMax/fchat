import "./message.css";

const Message = ({ message }) => {

    return (
        <div className={`message-container vbox ${message.is_mine ? 'mine' : 'theirs'}`}>
            <div className="message-sender">{message.sender}</div>
            <div className="message-text">{message.text}</div>
        </div>
    );
}

export default Message;