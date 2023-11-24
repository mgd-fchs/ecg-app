import React, { useState } from 'react';
import './TimerForm.css'; // make sure the path is correct

const TimerForm = () => {
  const [time, setTime] = useState('00:30');
  const [type, setType] = useState('normal');
  const [bpm, setBpm] = useState('60');
  const [fileUrl, setFileUrl] = useState('');

  // Handle "Download File"
  const handleDownload = () => {
    fetch(fileUrl)
      .then(response => response.blob())
      .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'recording_data.txt'); // This should match the file type you're expecting
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
      })
      .catch(e => console.error('Download error:', e));
  };
  
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
        setFileUrl(data.file_url);
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
        {/* Download button */}
        {fileUrl && (
        <button onClick={handleDownload}>Download File</button>
      )}
      </form>
    </div>
  );
};

export default TimerForm;
