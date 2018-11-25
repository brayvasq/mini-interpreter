import React from 'react'
import './User.css'
import axios from 'axios'

class User extends React.Component{

    constructor(props) {
        super(props)
        this.state = {
            id: this.props.id,
            username: this.props.username,
            email: this.props.email
        }
        this.delete = this.delete.bind(this);
    }

    componentDidMount() {
        //setInterval(this.getUsers,1000)
    }

    delete(){
        const token = localStorage.getItem("token");
        axios({
            method: 'delete',
            url: 'http://localhost:8000/api/users/'+this.state.id,
            headers: {
                Authorization: 'Bearer ' + token
            }
        }).then(resp => {
            console.log(resp);
        })
    }

    render() {
        return (
            <div className="margin-bt">
                <div className="box">
                    <article className="media">
                        <div className="media-left">
                            <figure className="image is-32x32">
                                <img className="is-rounded" src="https://www.qualiscare.com/wp-content/uploads/2017/08/default-user.png" alt="Image"/>
                            </figure>
                        </div>
                            <div className="content info-item">
                                <p>
                                    <strong>Username:</strong>&nbsp;{this.state.username}&nbsp;&nbsp;
                                    <strong>Email:</strong>&nbsp;{this.state.email}&nbsp;
                                </p>

                            </div>
                        <a className="button is-danger btn-item" onClick={this.delete}>Delete</a>
                    </article>

                </div>
            </div>
    );
    }

    }

    export default User;