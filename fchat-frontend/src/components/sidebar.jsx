import {useState, useEffect} from 'react';
import "./sidebar.css";

const Sidebar = () => {


    return (
        <div className="sidebar">
            <div className="sidebar-header">FChat</div>

            <div className="sidebar-login vbox">
                <input type="text" placeholder="Username" />
                <input type="password" placeholder="Password" />
                <button className="login-button" type="submit"> Login </button>
            </div>

            <div className="sidebar-create-chat hbox">
                <input type="text" placeholder="Chat Name" />
                <button> Create Chat </button>
            </div>

            <div className="sidebar-search vbox">
                <div className="search-header hbox">
                    <input type="text" placeholder="Search" />
                    <button> Search </button>
                </div>
                <div className="search-results vbox">
                    <div className="search-result">Result 1aedkhfguydfsdf</div>
                    <div className="search-result">Result 2aedkhfguydfsdf</div>
                    <div className="search-result">Result 3aedkhfguydfsdf</div>
                    <div className="search-result">Result 3aedkhfguydfsdf</div>
                    <div className="search-result">Result 3aedkhfguydfsdf</div>
                    <div className="search-result">Result 3aedkhfguydfsdf</div>
                    <div className="search-result">Result 3aedkhfguydfsdf</div>
                    <div className="search-result">Result 3aedkhfguydfsdf</div>
                    <div className="search-result">Result 3aedkhfguydfsdf</div>

                    <div className="search-result">Result 3</div>
                    <div className="search-result">Result 3</div>
                </div>
            </div>

            <div className="sidebar-chats vbox">
                <div className="chat-item">Chat 1</div>
                <div className="chat-item">Chat 2</div>
                <div className="chat-item">Chat 3</div>
            </div>
            
        </div>
    );
}

export default Sidebar;