import React, { useState } from 'react';
import axios from 'axios';

function AdminPanel() {
  const [username, setUsername] = useState('');
  const [amount, setAmount] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleBalanceAdjustment = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        'http://localhost:5000/admin/adjust_balance', 
        { username, amount: parseFloat(amount) },
        { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } }
      );
      setMessage(response.data.message);
      setError('');
      setUsername('');
      setAmount('');
    } catch (err) {
      setError(err.response?.data?.error || 'Balance adjustment failed');
      setMessage('');
    }
  };

  return (
    <div className="admin-panel-container">
      <h2>Byte Currency Admin Panel</h2>
      {message && <p className="success">{message}</p>}
      {error && <p className="error">{error}</p>}
      
      <form onSubmit={handleBalanceAdjustment}>
        <h3>Adjust User Balance</h3>
        <input 
          type="text" 
          placeholder="Username" 
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required 
        />
        <input 
          type="number" 
          placeholder="Amount to Add/Subtract" 
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          step="0.01"
          required 
        />
        <button type="submit">Adjust Balance</button>
      </form>
    </div>
  );
}

export default AdminPanel;
