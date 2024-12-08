import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Dashboard() {
  const [balance, setBalance] = useState(0);
  const [recipient, setRecipient] = useState('');
  const [amount, setAmount] = useState('');
  const [transactions, setTransactions] = useState({
    sent_transactions: [],
    received_transactions: []
  });
  const [error, setError] = useState('');

  useEffect(() => {
    fetchBalance();
    fetchTransactions();
  }, []);

  const fetchBalance = async () => {
    try {
      const response = await axios.get('http://localhost:5000/balance', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      setBalance(response.data.balance);
    } catch (err) {
      console.error('Error fetching balance', err);
    }
  };

  const fetchTransactions = async () => {
    try {
      const response = await axios.get('http://localhost:5000/transactions', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      setTransactions(response.data);
    } catch (err) {
      console.error('Error fetching transactions', err);
    }
  };

  const handleTransfer = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:5000/transfer', 
        { recipient, amount: parseFloat(amount) },
        { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } }
      );
      fetchBalance();
      fetchTransactions();
      setRecipient('');
      setAmount('');
      setError('');
    } catch (err) {
      setError(err.response?.data?.error || 'Transfer failed');
    }
  };

  return (
    <div className="dashboard-container">
      <h2>Byte Currency Dashboard</h2>
      <div className="balance-section">
        <h3>Your Balance: {balance.toFixed(2)} Bytes</h3>
      </div>

      <div className="transfer-section">
        <h3>Send Bytes</h3>
        {error && <p className="error">{error}</p>}
        <form onSubmit={handleTransfer}>
          <input 
            type="text" 
            placeholder="Recipient Username" 
            value={recipient}
            onChange={(e) => setRecipient(e.target.value)}
            required 
          />
          <input 
            type="number" 
            placeholder="Amount" 
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            min="0.01"
            step="0.01"
            required 
          />
          <button type="submit">Transfer</button>
        </form>
      </div>

      <div className="transactions-section">
        <h3>Transaction History</h3>
        <div className="sent-transactions">
          <h4>Sent Transactions</h4>
          {transactions.sent_transactions.map(transaction => (
            <div key={transaction.id} className="transaction">
              <p>To: {transaction.recipient_username}</p>
              <p>Amount: {transaction.amount} Bytes</p>
              <p>Date: {new Date(transaction.timestamp).toLocaleString()}</p>
            </div>
          ))}
        </div>
        <div className="received-transactions">
          <h4>Received Transactions</h4>
          {transactions.received_transactions.map(transaction => (
            <div key={transaction.id} className="transaction">
              <p>From: {transaction.sender_username}</p>
              <p>Amount: {transaction.amount} Bytes</p>
              <p>Date: {new Date(transaction.timestamp).toLocaleString()}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
