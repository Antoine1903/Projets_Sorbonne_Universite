import React, { useState } from 'react';

function EditMessage({ messageId, messageContent }) {
  const [newMessageContent, setNewMessageContent] = useState(messageContent);

  const handleEdit = () => {
    // 发送修改请求到服务器
    editMessage(messageId, newMessageContent);
  };

  return (
    <div>
      <textarea value={newMessageContent} onChange={(e) => setNewMessageContent(e.target.value)} />
      <button onClick={handleEdit}>Save</button>
    </div>
  );
}

export default EditMessage;
