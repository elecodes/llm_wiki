import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import UserChatView from './components/UserChatView';
import AdminView from './components/AdminView';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<UserChatView />} />
        <Route path="/admin" element={<AdminView />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
