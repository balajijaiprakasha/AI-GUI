import React, { useState, useRef } from "react";
import { Player } from "@lottiefiles/react-lottie-player";
import animation from "@/assets/assistant.json";
import "./App.css";

export default function TamilVoiceAssistant() {
  const [response, setResponse] = useState("");
  const [query, setQuery] = useState("");
  const [isListening, setIsListening] = useState(false);
  const playerRef = useRef();

  // Function to play audio with animation
  const playAudio = (url) => {
    const audio = new Audio(url);
    playerRef.current.play();
    audio.play();
    audio.onended = () => {
      playerRef.current.stop();
    };
  };

  const speak = async (text) => {
    const res = await fetch("http://127.0.0.1:5000/speak", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const data = await res.json();
    playAudio(`http://127.0.0.1:5000${data.audio_url}`);
  };

  const handleTextQuery = async () => {
    if (!query.trim()) return;
    setResponse("தயவு செய்து காத்திருக்கவும்...");
    const res = await fetch("http://127.0.0.1:5000/text-query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });
    const data = await res.json();
    setResponse(data.response);
    await speak(data.response);
  };

  const handleVoiceQuery = async () => {
    setIsListening(true);
    setResponse("கேட்கிறேன்...");
    const res = await fetch("http://127.0.0.1:5000/voice-query");
    const data = await res.json();
    setIsListening(false);
    setResponse(data.response);
    await speak(data.response);
  };

  return (
    <div className="assistant-container">
      <div className="assistant-card">
        <Player
          ref={playerRef}
          autoplay={false}
          loop
          src={animation}
          className="assistant-avatar"
        />
        <h2 className="assistant-title">தமிழ் உதவியாளர் 🤖</h2>
        <input
          className="assistant-input"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="உங்கள் கேள்வியை உள்ளிடவும்..."
        />
        <div className="assistant-buttons">
          <button className="btn btn-text" onClick={handleTextQuery}>
            Text கேள்வி
          </button>
          <button
            className={`btn ${isListening ? "btn-listening" : "btn-voice"}`}
            onClick={handleVoiceQuery}
            disabled={isListening}
          >
            {isListening ? "🎤 கேட்கிறேன்..." : "🎙️ Voice கேள்வி"}
          </button>
        </div>
        {response && <div className="assistant-response">{response}</div>}
      </div>
    </div>
  );
}
