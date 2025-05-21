import React, { useState } from 'react';

function UserSettings({ user }) {
  const [email, setEmail] = useState(user.email);
  const [password, setPassword] = useState('');
  const [notifications, setNotifications] = useState(user.notifications);

  const handleSaveSettings = () => {
    // 发送修改设置请求到服务器
    updateUserSettings(user.id, { email, password, notifications });
  };

  return (
    <div>
      <div>
        <label>Email</label>
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
      </div>
      <div>
        <label>Password</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      </div>
      <div>
        <label>Notifications</label>
        <input
          type="checkbox"
          checked={notifications}
          onChange={() => setNotifications(!notifications)}
        />
      </div>
      <button onClick={handleSaveSettings}>Save Settings</button>
    </div>
  );
}

export default UserSettings;
