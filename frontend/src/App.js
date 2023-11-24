import React from 'react';
import TimerForm from './components/TimerForm';
import './App.css'; // make sure the path is correct

function App() {
  return (
    <div className="App">
      <div className="App-header">Recording Generator</div>
      <TimerForm />
    </div>
  );
}

export default App;
