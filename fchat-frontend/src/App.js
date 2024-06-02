
import './App.css';
import Chat from './components/chat';
import Sidebar from './components/sidebar';

function App() {
  return (
    <div className="App hbox">
      <Sidebar />
      <Chat />
    </div>
  );
}

export default App;
