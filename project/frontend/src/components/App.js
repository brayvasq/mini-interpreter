import React, {Component} from 'react';
import './App.css';


class App extends Component {
    render() {
        return (
            <div className="login">

                <div className="container has-text-centered">
                    <div className="column is-4 is-offset-4">
                        <div className="center">

                            <div className="box">
                                <h1 className="title is-1"> Hello </h1>
                                <form>
                                    <div className="field">
                                        <div className="control">
                                            <input className="input" type="email" placeholder="Your Email"
                                                   autoFocus=""/>
                                        </div>
                                    </div>
                                    <div className="field">
                                        <div className="control">
                                            <input className="input" type="email" placeholder="Your Email"
                                                   autoFocus=""/>
                                        </div>
                                    </div>
                                    <button className="button is-primary"> Sign In</button>
                                    <button className="button is-primary">Sign Up</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default App;