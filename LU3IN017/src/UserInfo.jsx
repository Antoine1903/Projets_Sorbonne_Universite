import React from 'react';

function UserInfo({ user }) {
  return (
    <div>
      <h3>{user.name}</h3>
      <p>Email: {user.email}</p>
      <p>Joined: {user.joinDate}</p>
    </div>
  );
}

export default UserInfo;
