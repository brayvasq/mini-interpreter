import React from 'react';
import './NavBar.css'
import axios from "axios";

class NavBar extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            create: this.props.create
        };
        this.logout = this.logout.bind(this);
        this.create = this.create.bind(this);
    }

    logout() {
        localStorage.removeItem("token");
        //this.props.history.push("/app");
        window.location = '/app'
    }

    create(){
        const token = localStorage.getItem("token");
        axios({
            method: 'post',
            url: 'http://localhost:8000/api/sentences',
            data:{
              input_code: "0"
            },
            headers: {
                Authorization: 'Bearer ' + token
            }
        }).then(resp => {
            console.log(resp);
        })
    }

    render() {

        return (
            <div className="nav-bar">
                <nav className="navbar" role="navigation" aria-label="main navigation">
                    <div className="navbar-brand">
                        <a className="navbar-item" href="https://bulma.io">
                            <img src="https://bulma.io/images/bulma-logo.png" width="112" height="28"/>
                        </a>

                        <a role="button" className="navbar-burger burger" aria-label="menu" aria-expanded="false"
                           data-target="navbarBasicExample">
                            <span aria-hidden="true"></span>
                            <span aria-hidden="true"></span>
                            <span aria-hidden="true"></span>
                        </a>
                    </div>

                    <div id="navbarBasicExample" className="navbar-menu">
                        <div className="navbar-start">
                            <a className="navbar-item">
                                Home
                            </a>

                            <a className="navbar-item">
                                Documentation
                            </a>
                        </div>

                        <div className="navbar-end">
                            <div className="navbar-item">
                                <div className="buttons">

                                    {this.state.create ? <a className="button" onClick={this.create}>
                                        <strong>Create</strong>
                                    </a> : <div></div>}
                                    <a className="button is-primary" onClick={this.logout}>
                                        <strong>Logout</strong>
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </nav>
            </div>
        );
    }
}

export default NavBar;