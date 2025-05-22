import { useState, useEffect } from "react";
import axios from "axios";
import serverConfig from "./api/serverConfig.jsx";
import ReplyList from "./ReplyList.jsx";
import DeleteMessage from "./DeleteMessage.jsx";
import EditMessage from "./EditMessage.jsx";

function Message(props) {
  const [author, setAuthor] = useState(null);
  const [replies, setReplies] = useState([]);
  const [replyCount, setReplyCount] = useState(0);
  const [likeCount, setLikeCount] = useState(props.messageInfo.likes.length);
  const [userHasLiked, setUserHasLiked] = useState(
    props.messageInfo.likes.includes(props.currentUser.uid)
  );

  useEffect(() => {
    const getAuthor = async () => {
      try {
        let response = await serverConfig(
          axios.get,
          `/api/user/${props.messageInfo.uid}`
        );
        setAuthor(response.data);
      } catch (err) {
        console.error(err);
      }
    };
    getAuthor();
  }, [props.messageInfo.uid]);

  const getReplies = async () => {
    try {
      let response = await serverConfig(
        axios.get,
        `/api/reply?mid=${props.messageInfo.mid}`
      );
      setReplies(response.data);
      setReplyCount(response.data.length);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    getReplies();
  }, [props.messageInfo.mid]);

  const addReply = (event) => {
    event.preventDefault();
    let content = document.getElementById(`reply-${props.messageInfo.mid}`);
    if (content.value.length > 0) {
      let user = props.currentUser;
      let message = props.messageInfo;
      serverConfig(axios.put, "/api/reply", {
        content: content.value,
        uid: user.uid,
        mid: message.mid,
      })
        .then((result) => {
          let rid = result.data.details.rid;
          return serverConfig(axios.get, `/api/reply/${rid}`);
        })
        .then((response) => {
          let reply = response.data;
          setReplies([...replies, reply]);
          getReplies();
        })
        .catch((err) => {
          console.error(err);
        });
      content.value = "";
    }
  };

  const removeReply = (rid) => {
    serverConfig(axios.delete, `/api/reply/${rid}`)
      .then((result) => {
        setReplies(replies.filter((reply) => reply.rid !== rid));
        getReplies();
      })
      .catch((err) => {
        console.error(err);
      });
  };

  const like = () => {
    serverConfig(axios.patch, "/api/likes/message", {
      mid: props.messageInfo.mid,
      uid: props.currentUser.uid,
    })
      .then((result) => {
        setLikeCount(result.data.details.count);
        setUserHasLiked(!userHasLiked);
      })
      .catch((err) => {
        console.error(err);
      });
  };

  let date = new Date(props.messageInfo.date);
  let formattedDate = `${date
    .getDate()
    .toString()
    .padStart(2, "0")}/${(date.getMonth() + 1).toString().padStart(2, "0")}/${
    date.getFullYear()
  }`;

  return (
    <div className="message-container">
      <h3>{props.messageInfo.title}</h3>
      <p>{props.messageInfo.content}</p>
      <div className="message-info">
        Publié le {formattedDate} par{" "}
        <a onClick={() => props.toUserPage(author)}>
          {author ? author.uname : ""}
        </a>
      </div>

      <div className="message-icons">
        <div className="message-icon">
          <button type="button" className="btn-icon" onClick={like}>
            {userHasLiked ? (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                fill="currentColor"
                className="message-icon bi bi-heart-fill"
                viewBox="0 0 16 16"
              >
                <path
                  fillRule="evenodd"
                  d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314"
                />
              </svg>
            ) : (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                fill="currentColor"
                className="message-icon bi bi-heart"
                viewBox="0 0 16 16"
              >
                <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143q.09.083.176.171a3 3 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15" />
              </svg>
            )}
          </button>
          {likeCount}
        </div>

        <div className="message-icon">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            fill="currentColor"
            className="message-icon bi bi-reply-fill"
            viewBox="0 0 16 16"
          >
            <path d="M5.921 11.9 1.353 8.62a.72.72 0 0 1 0-1.238L5.921 4.1A.716.716 0 0 1 7 4.719V6c1.5 0 6 0 7 8-2.5-4.5-7-4-7-4v1.281c0 .56-.606.898-1.079.62z" />
          </svg>
          {replyCount}
        </div>

        {props.messageInfo.uid === props.currentUser.uid && (
          <DeleteMessage
            onDelete={props.removeMessage}
            id={props.messageInfo.mid}
          />
        )}
      </div>

      <ReplyList
        replies={replies}
        removeReply={removeReply}
        currentUser={props.currentUser}
        toUserPage={props.toUserPage}
      />

      <form className="new-reply">
        <div>
          <label htmlFor={`reply-${props.messageInfo.mid}`}>
            Votre réponse
          </label>
          <textarea
            className="reply-content"
            id={`reply-${props.messageInfo.mid}`}
            placeholder="Veuillez saisir votre message de réponse"
          ></textarea>
        </div>
        <button type="button" className="reply-button" onClick={addReply}>
          Ajouter une réponse
        </button>
      </form>
    </div>
  );
}

export default Message;
