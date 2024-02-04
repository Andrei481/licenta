import React, {useState} from "react";
import "./Home.css"

const Home = () => {
    const [inputMessage, setInputMessage] = useState("");

    const handleSendMessage = () => {
        console.log("User: " + inputMessage);
        setInputMessage(""); // clear after message is sent
    };

    return (
        <div className="home-container">
          <header>
            <h1>My Simple React Home Page</h1>
          </header>
          <div className="bottom-container">
            <input type="text"
                placeholder="Send message..."
                value={inputMessage}
                onChange={ event => setInputMessage(event.target.value) }
            />
            <button onClick={handleSendMessage}>
                Send!
            </button>
          </div>
        </div>
      );
};

export default Home;