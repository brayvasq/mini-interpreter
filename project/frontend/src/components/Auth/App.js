import React, {Component} from 'react';
import './App.css';
import axios from 'axios';

class App extends Component {

    constructor(props) {
        super(props)
        this.state = {
            username: '',
            password: ''
        }
        this.register = this.register.bind(this);
        this.login = this.login.bind(this);
        this.handleChangeUser = this.handleChangeUser.bind(this);
        this.handleChangePass = this.handleChangePass.bind(this);
    }

    handleChangeUser(event) {
        this.setState({username: event.target.value})
    }

    handleChangePass(event) {
        this.setState({password: event.target.value})
    }

    login(){
        const dataUser = {
            username: this.state.username,
            password: this.state.password
        }
        axios.post('http://localhost:8000/api/auth/login/',dataUser).then(resp =>{
            console.log(resp)
            if(resp.data.token){
                localStorage.setItem("token",resp.data.token);
                if(resp.data.is_coder){
                    this.props.history.push("/code");
                }else{
                    this.props.history.push("/users");
                }
            }

        });
    }

    register() {
        const dataUser = {
            username: this.state.username,
            password: this.state.password,
            email: this.state.username + "@mail.com",
            is_coder: true,
            is_reviewer: false
        }
        axios.post('http://localhost:8000/api/auth/register/',dataUser).then(resp =>{
            console.log(resp)
        });
    }

    render() {
        return (
            <div className="login">

                <div className="container has-text-centered">
                    <div className="column is-4 is-offset-4">
                        <div className="box center">
                            <h1 className="title is-1"> Interpreter </h1>
                            <form>
                                <div className="field">
                                    <label className="label">UserName</label>
                                    <div className="control">
                                        <input className="input" type="text" placeholder="Username" value={this.state.username} onChange={this.handleChangeUser}/>
                                    </div>
                                </div>
                                <div className="field">
                                    <label className="label">Password</label>
                                    <div className="control">
                                        <input className="input" type="password" placeholder="Password" value={this.state.password} onChange={this.handleChangePass}/>
                                    </div>
                                </div>

                                <div className="buttons">
                                    <span className="button is-success" onClick={this.login}>Sing In</span>
                                    <span className="button is-info" onClick={this.register}>Sign Up</span>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default App;