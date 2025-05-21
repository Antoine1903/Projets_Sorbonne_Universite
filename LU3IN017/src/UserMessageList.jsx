import React, { useState, useEffect } from 'react';
import Message from './Message';

function UserMessageList({ userId }) {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    // 获取用户发布的消息
    const fetchUserMessages = async () => {
      const userMessages = await getUserMessages(userId);
      setMessages(userMessages);
    };

    fetchUserMessages();
  }, [userId]);

  return (
    <div>
      <h4>Messages</h4>
      {messages.map((message) => (
        <Message key={message.id} {...message} />
      ))}
    </div>
  );
}

export default UserMessageList;
