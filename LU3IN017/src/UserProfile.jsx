import React from "react";
import AddMessage from "./AddMessage.jsx";

function UserProfile({ user, currentUser, addMessage }) {
  return (
    <div>
      {user.uid === currentUser.uid ? (
        <div className="box">
          <h2>Nouveau message</h2>
          <AddMessage addMessage={addMessage} />
        </div>
      ) : (
        ""
      )}
    </div>
  );
}

export default UserProfile;
