import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import { Route, Link, BrowserRouter as Router } from 'react-router-dom'
import App from "./components/App";
import Users from "./components/Users"
import Code from "./components/Code"

const routing = (
    <Router>
        <div>
            <Route path="/app" component={App}></Route>
            <Route path="/users" component={Users}></Route>
            <Route path="/code" component={Code}></Route>
        </div>
    </Router>
)

ReactDOM.render(routing, document.getElementById('app'));