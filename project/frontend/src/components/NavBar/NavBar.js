import React from 'react';
import './NavBar.css'

class NavBar extends React.Component{
    constructor(props){
        super(props)
        this.logout = this.logout.bind(this);
    }

    logout(){
        localStorage.removeItem("token");
        //this.props.history.push("/app");
        window.location = '/app'
    }

    render(){
        return(
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