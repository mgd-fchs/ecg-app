import React, { useState } from 'react';
import './TimerForm.css'; 

const TimerForm = () => {
  const [time, setTime] = useState('00:30');
  const [type, setType] = useState('normal');
  const [bpm, setBpm] = useState('60');
  const [fileUrl, setFileUrl] = useState('');
  const [showToast, setShowToast] = useState(false); 
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState(''); // For differentiating between error and success messages

  const Toast = ({ message, type }) => {
    return (
      <div className={`toast-message ${type === 'success' ? 'success' : 'error'}`}>
        {message}
      </div>
    );
  };

  // Handle "Download File"
  const handleDownload = () => {
    fetch(fileUrl)
      .then(response => response.blob())
      .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'recording_data.csv');
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
      })
      .catch(e => console.error('Download error:', e));
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    setShowToast(false); // Hide toast before new submission
    // Clear previous messages
    setMessage('');
    setMessageType('');
  
    // Data to be sent to the backend
    const data = { time, type, bpm };
  
    // Send a POST request with the fetch API
    fetch('http://localhost:5000/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
    .then(response => {
      // Check if the response was ok (status code 200-299)
      if (!response.ok) {
        // If response is not ok, we still want to parse the JSON body
        // to get the error message sent from the server
        return response.json().then(errData => {
          throw new Error(errData.message || 'Something went wrong.');
        });
      }
      return response.json();
    })
    .then(data => {
      if (data.status === 'success') {
        setFileUrl(data.file_url);
        setMessage(data.message);
        setMessageType('success');
      } else {
        setMessage(data.message || 'An unknown error occurred.');
        setMessageType('error');
      }
    })
    .catch((error) => {
      setMessage(error.message || 'An error occurred while processing your request.');
      setMessageType('error');
    })
    .finally(() => {
      setShowToast(true); // Show toast after submission
      setTimeout(() => {
        setShowToast(false); // Hide toast after 3 seconds
      }, 3000);
    });
  };

  
  
  return (
    <div className="form-container"> {}
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
      {showToast && <Toast message={message} type={messageType} />}
    </div>
  );
};

export default TimerForm;
