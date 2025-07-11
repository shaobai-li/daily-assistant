import './ChatInput.css';
import { useState } from 'react';
import sendButton from './icons8-send-button-90.png';

export default function ChatInput() {
  const [inputValue, setInputValue] = useState('');

  return (
    <div className="chat-input">
      <input
        type="text"
        className="input-field"
        placeholder="Ask anything"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
      />
      <div className="chat-button-container">
        <button 
        className="send-button">
          <img src={sendButton} alt="Send" width={20} height={20}/>
        </button>
      </div>
    </div>
  )
}