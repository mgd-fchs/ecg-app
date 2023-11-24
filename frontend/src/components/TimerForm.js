import React, { useState } from 'react';
import './TimerForm.css'; // make sure the path is correct

const TimerForm = () => {
  const [time, setTime] = useState('00:30');
  const [type, setType] = useState('normal');
  const [bpm, setBpm] = useState('60');
  const [filePath, setFilePath] = useState('');
  
  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Data to be sent to the backend
    const data = { time, type, bpm };

    // Send a POST request with the fetch API
    fetch('http://localhost:5000/generate', { // make sure the URL points to your Flask server
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
    .then(response => response.json()) // assuming your Flask server responds with JSON
    .then(data => {
      console.log('Success:', data);
      if (data.status === 'success') {
        // Set the file path if file creation was successful
        setFilePath(data.file_path);
      }
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  };

  return (
    <div className="form-container"> {/* Apply the style here */}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Length of Recording (min:seconds): </label>
          <input
            type="text"
            value={time}
            onChange={(e) => setTime(e.target.value)}
            placeholder="min:seconds"
            required
          />
        </div>
        <div>
          <label>Type: </label>
          <select value={type} onChange={(e) => setType(e.target.value)}>
            <option value="normal">Normal</option>
            <option value="arrhythmia">Arrhythmia</option>
          </select>
        </div>
        <div>
          <label>BPM: </label>
          <input
            type="int"
            value={bpm}
            onChange={(e) => setBpm(e.target.value)}
            placeholder="60"
            required
          />
        </div>
        <button type="submit">Generate</button>
        {/* Conditionally render the download button */}
        {filePath && (
          <a href={filePath} download>
            <button type="button">Download File</button>
          </a>
        )}
      </form>
    </div>
  );
};

export default TimerForm;
