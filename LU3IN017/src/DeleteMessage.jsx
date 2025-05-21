import React from 'react';

function DeleteMessage({ messageId, author, currentUser, onDelete }) {
  const canDelete = currentUser?.isAdmin || currentUser?.username === author;

  if (!canDelete) return null;

  const handleClick = () => {
    if (window.confirm("Are you sure you want to delete this message?")) {
      onDelete(messageId);
    }
  };

  return <button onClick={handleClick}>Delete</button>;
}

export default DeleteMessage;
