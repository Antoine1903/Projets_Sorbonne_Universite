import { useState, useRef } from "react";
import axios from 'axios';
import serverConfig from "./api/serverConfig.jsx";

function Login(props) {
    // Login modal
    const domModal = useRef(null);

    const modalOpen = () => {
        domModal.current.style.display = "block";
    };

    const modalClose = () => {
        domModal.current.style.display = "none";
    };

    // Login form
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const getUsername = (event) => {
        setUsername(event.target.value);
    };

    const getPassword = (event) => {
        setPassword(event.target.value);
    };

    // Message
    const [alert, setAlert] = useState(null);

    // Handle login
    const handleLogin = () => {
        if (username && password) {
            serverConfig(axios.post, '/api/authentification', {
                uname: username,
                password: password
            }).then((result) => {
                let user = result.data.details.user;
                setAlert(null);
                props.login(user);
            }).catch((err) => {
                console.error(err);
                setAlert(err.response.data.message);
            });
        } else {
            setAlert("Les informations saisies sont incomplètes.");
        }
    };

    return (
        <div className="login-container">
            <button id="login-btn" onClick={modalOpen}>Se connecter</button>
            <div className="modal" ref={domModal}>
                <div className="modal-content">
                    <span className="modal-close" onClick={modalClose}>&times;</span>
                    <h2>Se connecter</h2>
                    {alert && <div className='alert error'>{alert}</div>}
                    <form id="login" method="post" action="">
                        <div className="form-group">
                            <label htmlFor="username">Identifiant</label>
                            <input
                                type="text"
                                id="username"
                                placeholder="Identifiant"
                                onChange={getUsername}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="password">Mot de passe</label>
                            <input
                                type="password"
                                id="password"
                                placeholder="Mot de passe"
                                onChange={getPassword}
                                required
                            />
                        </div>
                        <button type="button" onClick={handleLogin}>Connexion</button>
                    </form>
                </div>
            </div>
        </div>
    );
}

export default Login;
