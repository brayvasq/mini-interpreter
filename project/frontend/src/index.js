import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import { Route, Link, BrowserRouter as Router } from 'react-router-dom'
import App from "./components/App";
import Users from "./components/Users"

const routing = (
    <Router>
        <div>
            <Route path="/app" component={App}></Route>
            <Route path="/users" component={Users}></Route>
        </div>
    </Router>
)

ReactDOM.render(routing, document.getElementById('app'));