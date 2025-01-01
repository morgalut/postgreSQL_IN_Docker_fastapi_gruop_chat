import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [users, setUsers] = useState([]);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [selectedUserId, setSelectedUserId] = useState('');
  const [newUser, setNewUser] = useState({ username: '', email: '' });

  useEffect(() => {
    fetchUsers();
    fetchMessages();
  }, []);

  const fetchUsers = async () => {
    const response = await axios.get('http://localhost:8000/users/');
    setUsers(response.data);
  };

  const fetchMessages = async () => {
    const response = await axios.get('http://localhost:8000/messages/');
    setMessages(response.data);
  };

  const sendMessage = async () => {
    if (!selectedUserId) {
      alert('Select a user first!');
      return;
    }
    await axios.post('http://localhost:8000/messages/', {
      user_id: selectedUserId,
      content: newMessage
    });
    setNewMessage('');
    fetchMessages(); // Reload messages
  };

  const registerUser = async () => {
    if (!newUser.username || !newUser.email) {
      alert('Username and email are required!');
      return;
    }
    try {
      await axios.post('http://localhost:8000/users/', newUser);
      alert('User registered successfully');
      setNewUser({ username: '', email: '' });
      fetchUsers();
    } catch (error) {
      alert('Failed to register user');
      console.error('Registration error:', error);
    }
  };

  return (
    <div>
      <h1>Group Chat</h1>
      <div>
        <h2>Register User</h2>
        <input
          type="text"
          placeholder="Username"
          value={newUser.username}
          onChange={(e) => setNewUser({...newUser, username: e.target.value})}
        />
        <input
          type="email"
          placeholder="Email"
          value={newUser.email}
          onChange={(e) => setNewUser({...newUser, email: e.target.value})}
        />
        <button onClick={registerUser}>Register</button>
      </div>
      <div>
        <h2>Users</h2>
        {users.map(user => (
          <button key={user.user_id} onClick={() => setSelectedUserId(user.user_id)}>
            {user.username}
          </button>
        ))}
      </div>
      <div>
        <h2>Messages</h2>
        {messages.map(message => (
          <p key={message.message_id}><strong>{findUserName(message.user_id)}:</strong> {message.content}</p>
        ))}
      </div>
      <div>
        <textarea
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
        />
        <button onClick={sendMessage}>Send Message</button>
      </div>
    </div>
  );

  function findUserName(userId) {
    const user = users.find(user => user.user_id === userId);
    return user ? user.username : 'Unknown user';
  }
}

export default App;
