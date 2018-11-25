import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import { Route, Link, BrowserRouter as Router } from 'react-router-dom'
import App from "./components/Auth/App";
import ListUsers from "./components/Users/ListUsers"
import Code from "./components/Code/Code"

const routing = (
    <Router>
        <div>
            <Route path="/app" component={App}></Route>
            <Route path="/users" component={ListUsers}></Route>
            <Route path="/code" component={Code}></Route>
        </div>
    </Router>
)

ReactDOM.render(routing, document.getElementById('app'));