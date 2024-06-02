import {useState, useEffect} from 'react';
import "./sidebar.css";

const SidebarLogin = ({ user, setUser, setPassword }) => {
    if (user) {
        return (
            <div className="sidebar-login">
                <div className="sidebar-username">{user}</div>
                <button className="logout-button" onClick={
                    () => {
                        setUser(null);
                        setPassword(null);
                    }
                    }> Logout </button>
            </div>
        );
    } else {
        return (
            <div className="sidebar-login vbox">
                <input type="text" id="username" placeholder="Username" />
                <input type="password" id="password" placeholder="Password" />
                
                <button className="login-button" type="submit" onClick={
                    () => {
                        let username = document.getElementById("username").value;
                        let password = document.getElementById("password").value;

                        if (username && password) {
                            setUser(username);
                            setPassword(password);
                        }
                    }
                } > Login </button>
            </div>
        );
    }
}

const SidebarSearch = ({ setChat_id }) => {
    const [search, setSearch] = useState("");
    const [results, setResults] = useState([]);
    
    useEffect(() => {
        if (search) {
            // fetch search results
            // setResults([...]);

            var fake_results = [
                {name: "Result 1", id: 1},
                {name: "Result 2", id: 2},
                {name: "Result 3", id: 3},
            ];
            setResults(fake_results);
        }
    }, [search]);

    

    return (
        <div className="sidebar-search vbox">
            <div className="search-header hbox">
                <input type="text" placeholder="Search" value={search} onChange={(e) => setSearch(e.target.value)} />
            </div>
            <div className="search-results vbox">
                {results.map((result) => {
                    return <div className="search-result" key={result.id} onClick={() => setChat_id(result.id)}>{result.name}</div>
                })}
            </div>
        </div>
    );
}

const Sidebar = ({ user, setUser, setPassword, setChat_id, sidebarChats }) => {
    return (
        <div className="sidebar">
            <div className="sidebar-header">FChat</div>

            <SidebarLogin user={user} setUser={setUser} setPassword={setPassword} />

            <div className="sidebar-create-chat hbox">
                <input type="text" placeholder="Chat Name" />
                <button> Create Chat </button>
            </div>

            <SidebarSearch setChat_id={setChat_id} />

            <div className="sidebar-chats vbox">
                {sidebarChats.map((chat, index) => {
                    return <div className="chat-item" key={index} onClick={() => setChat_id(chat.id)}>{chat.name}</div>
                })
                }
            </div>
            
        </div>
    );
}

export default Sidebar;