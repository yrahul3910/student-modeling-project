import React from "react";
import { Switch, Route } from "react-router-dom";

import MainPage from "./MainPage.jsx";
import Login from "./Login.jsx";
import Register from "./Register.jsx";

class App extends React.Component {
    constructor(props) {
        super(props);
        this.toggleLogin = this.toggleLogin.bind(this);
        this.state = { user: null };
    }

    toggleLogin(user) {
        this.setState({ user });
    }

    render() {
        return (
            <Switch>
                <Route exact path="/" render={(props) =>
                    <MainPage {...props} toggleLogin={this.toggleLogin} />
                } />
                <Route exact path="/login" render={(props) =>
                    <Login {...props} toggleLogin={this.toggleLogin} />
                } />
                <Route exact path="/register" render={(props) =>
                    <Register {...props} toggleLogin={this.toggleLogin} />
                } />
            </Switch>
        );
    }
}

export default App;
