import React from "react";
import PropTypes from "prop-types";
import { Link } from "react-router-dom";
import Banner from "./Banner.jsx";

class MainPage extends React.Component {
    constructor(props) {
        super(props);
        this.state = { name: null, type: null };
    }

    async componentDidMount() {
        // If logged in, take user to dashboard
        const token = localStorage.getItem("token");
        if (token) {
            const response = await fetch("/api/user/details", {
                method: "POST",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    token
                })
            });
            const data = await response.json();
            let { user } = data;

            this.props.toggleLogin(user);
            this.setState({ name: user.name, type: user.type })
        }
    }

    render() {
        let loginButton;
        if (!this.state.name)
            loginButton = (
                <div className="center">
                    <Link to="/login" className="btn waves-effect waves-light white-text" style={{ marginRight: "40px" }} >
                        LOG IN
                    </Link>
                    <Link to="/register" className="btn waves-effect waves-light white-text" >
                        SIGN UP
                    </Link>
                </div>
            );
        else
            loginButton = (
                <div className="center">
                    <Link to="/user" className="teal-text"
                        style={{ fontSize: 16, fontWeight: 400 }}>
                        Welcome back, {this.state.name}! Continue to your dashboard.
                    </Link>
                </div>
            );
        return (
            <div>
                <div className="left-shift">
                    <h2 style={{ color: "#404040" }}>Get started today. It&apos;s free, forever.</h2>
                </div>
                {loginButton}
            </div>
        );
    }
}

MainPage.propTypes = {
    toggleLogin: PropTypes.func.isRequired
};

export default MainPage;
