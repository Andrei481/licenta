import React, {useState} from "react";
import "./Home.css"
import axios from "axios";

const url = "http://localhost:8080"; // using 8080 since vllm api is running on 8000
const vllm_url = "http://localhost:8000/generate"

const Home = () => {
    const [userMessage, setUserMessage] = useState("");
    const [messages, setMessages] = useState([]);

    const sendMessage = () => {
      setMessages((prevMessages) => [
        ...prevMessages,
        { type: "input", message: userMessage },
      ]);
        console.log("User: " + userMessage);
        const req = {
          "prompt": userMessage,
          "n": 1,
          "temperature": 0.95,
          "max_tokens": 200
        }
        axios.post(url + "/inference", req)
        .then(response => {
          const assistantResponse = response.data.text[0];
          setMessages((prevMessages) => [
            ...prevMessages,
            { type: "input", message: userMessage },
            { type: "output", message: assistantResponse },
          ]);
          console.log("Output: " + response.data.text[0]);
        })
        .catch(error => {
          console.log("Error: " + error);
        });
        setUserMessage("");
    };

    return (
        <div className="home-container">
          <header>
            <h1>ChatUPT</h1>
          </header>
          <div className="chat-container">
          {messages.map((msg, index) => (
            <div key={index} className={`${msg.input}`}>
              <div className="message-container">
              <h2>
                {(() => {
                  if (msg.type === "input") {
                    return "User";
                  } else {
                    return "Assistant";
                  }
                })()}
              </h2>
              <p>{msg.message}</p>
              </div>
            </div>
          ))}
          </div>
          <div className="bottom-container">
            <input type="text"
                placeholder="Send message..."
                value={userMessage}
                onChange={ event => setUserMessage(event.target.value) }
            />
            <button onClick={sendMessage}>
                Send!
            </button>
          </div>
        </div>
      );
};

export default Home;