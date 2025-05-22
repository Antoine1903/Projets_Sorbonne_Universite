import { useState, useEffect } from "react";
import axios from "axios";
import serverConfig from "./api/serverConfig.jsx";
import {
  getMessagesRequest,
  addMessageRequest,
  removeMessageRequest,
} from "./api/messagesAPI.jsx";
import UserInfo from "./UserInfo.jsx";
import UserMessageList from "./UserMessageList.jsx";
import UserProfile from "./UserProfile.jsx";
import UserSettings from "./UserSettings.jsx";

function User(props) {
  const [messages, setMessages] = useState([]);
  const [isAdmin, setIsAdmin] = useState(props.user.user.admin);

  useEffect(() => {
    getMessagesRequest(
      setMessages,
      props.user.user.uid,
      props.currentUser.admin ? "" : "0"
    );
  }, []);

  const addMessage = (event) => {
    addMessageRequest(event, props, messages, setMessages, false);
  };

  const removeMessage = (mid) => {
    removeMessageRequest(messages, setMessages, mid);
  };

  const setAdmin = () => {
    if (props.user.user.uid !== props.currentUser.uid) {
      const status = !isAdmin;
      serverConfig(axios.patch, "api/admin", {
        uid: props.user.user.uid,
        status: status,
      })
        .then(setIsAdmin(status))
        .catch(console.error);
    }
  };

  return (
    <main>
      <div id="back-to-index">
        <a onClick={props.toFeedPage}>❮ Retour à l'accueil</a>
      </div>

      <UserInfo
        user={props.user.user}
        currentUser={props.currentUser}
        setAdmin={setAdmin}
        isAdmin={isAdmin}
      />

      <UserProfile
        user={props.user.user}
        currentUser={props.currentUser}
        addMessage={addMessage}
      />

      <UserMessageList
        messages={messages}
        removeMessage={removeMessage}
        currentUser={props.currentUser}
        toUserPage={props.toUserPage}
      />

      <UserSettings
        user={props.user.user}
        currentUser={props.currentUser}
        setAdmin={setAdmin}
        isAdmin={isAdmin}
      />
    </main>
  );
}

export default User;
