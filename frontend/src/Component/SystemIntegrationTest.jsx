import { useEffect, useState } from 'react';
import axios from 'axios';

function SystemIntegrationTest() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    // Note the full path: base + prefix + endpoint
    axios.get('http://localhost:8000/api/test/')
      .then(res => {
        setMessage(res.data.message);
      })
      .catch(err => console.error("Check if Django is running!", err));
  }, []);

  return (
    <div>
      <h1>Vite + Django</h1>
      <p>Response: {message}</p>
    </div>
  );
}

export default SystemIntegrationTest;