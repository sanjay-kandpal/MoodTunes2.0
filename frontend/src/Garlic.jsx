import React, { useContext } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import Bgm from './components/bgm.mp4';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from './AuthContext'; // Import the context
import './index.css'
function Garlic() {
    const { isLoggedIn } = useContext(AuthContext); // Access the context
    const navigate = useNavigate();

    const handleLogin = () => {
        navigate('/login');
    };

    return (
        <div>
            <nav className="navbar navbar-expand-lg navbar-light bg-dark" style={{ paddingLeft: "20px" }}>
                <h1 className="navbar-brand logo"></h1>
                <div className="collapse navbar-collapse" id="navbarNav">
                    <ul className="navbar-nav">
                        <li className="nav-item active">
                            <a className="nav-link" id="home" href="http://localhost:3000/home">Home</a>
                        </li>
                        <li className="nav-item">
                            <a className="nav-link" id="abt-us" href="http://localhost:3000/about">About-Us</a>
                        </li>
                    </ul>
                </div>
            </nav>
            <video loop autoPlay muted id="myvideo">
                <source src={Bgm}></source>
            </video>
            <div>
                <h1 id="abt" className='text-xl'>Introducing MoodTunes</h1>
                <p id="abt2">
                    <center>
                        We’ve trained a model called MoodTunes which reads facial expressions
                        <br></br>and plays songs to lighten the mood.
                    </center>
                </p>
            </div>
            {isLoggedIn ? (
                <a href="http://127.0.0.1:5000/" id="abt3" target="_blank">Try MoodTunes</a>
            ) : (
                <button onClick={handleLogin} id="abt3">Login</button>
            )}
        </div>
    );
}

export default Garlic;
