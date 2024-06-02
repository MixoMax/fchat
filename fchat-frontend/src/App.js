
import './App.css';
import Chat from './components/chat';
import Sidebar from './components/sidebar';

import {useEffect, useState} from 'react';

function App() {
  const [user, setUser] = useState(null);
  const [password, setPassword] = useState(null);
  const [key, setKey] = useState(null);
  const [chat_id, setChat_id] = useState(null);
  const [chat_messages, setChatMessages] = useState([]);
  const [sidebarChats, setSidebarChats] = useState([]);

  const api_url = "http://localhost:8000";

  useEffect(() => {
    if (chat_id) {
      var url = `${api_url}/chats/exists?chat_id=${chat_id}`;
      fetch(url)
        .then(response => response.json())
        .then(data => {
          if (data.exists) {
            
            var url = `${api_url}/chats/get?chat_id=${chat_id}`;
            fetch(url)
              .then(response => response.json())
              .then(data => {
                setChatMessages(data.messages);
              });

          }
        });
    }
  }, [chat_id]);

  useEffect(() => {
    var url = `${api_url}/chats/get?user_id=${user}`;
    if (user) {
      fetch(url)
        .then(response => response.json())
        .then(data => {
          setSidebarChats(data.chats);
        });
    }
  }, [user]);

  useEffect(() => {
    if (user && password) {
      var url = `${api_url}/users/auth?name=${user}&password=${password}`;
      fetch(url)
        .then(response => response.json())
        .then(data => {
          if (data.auth) {
            setKey(data.key);
            console.log("Logged in as " + user);
            console.log("Key: " + key);
          }
        });
    }
  }, [user, password]);

  return (
    <div className="App hbox">
      <Sidebar user={user} setUser={setUser} setPassword={setPassword} setChat_id={setChat_id} sidebarChats={sidebarChats} />
      <Chat chat_id={chat_id} setChat={setChat_id} chat_messages={chat_messages} setChatMessages={setChatMessages} user={user} />
    </div>
  );
}

export default App;
