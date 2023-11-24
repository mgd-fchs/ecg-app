import React from 'react';
import TimerForm from './components/TimerForm';
import './App.css'; // make sure the path is correct

function App() {
  return (
    <div className="App">
      <h1>Recording Generator</h1>
      <TimerForm />
    </div>
  );
}

export default App;
