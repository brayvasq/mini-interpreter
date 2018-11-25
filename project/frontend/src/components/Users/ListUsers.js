import React from 'react'
import NavBar from '../NavBar/NavBar'
import axios from 'axios'
import './ListUsers.css'
import User from './User'

class ListUsers extends React.Component {

    constructor(props) {
        super(props)

        this.state = {
            list: []
        };

        this.getUsers = this.getUsers.bind(this);
        this.createdTasks = this.createdTasks.bind(this);
    }

    componentDidMount() {
        setInterval(this.getUsers,1000)
        //this.getUsers()
    }

    createdTasks(item) {
        return <User key={item.id} id={item.id} username={item.username} email={item.email}/>
    }

    getUsers() {
        const token = localStorage.getItem("token");
        axios({
            method: 'get',
            url: 'http://localhost:8000/api/users',
            headers: {
                Authorization: 'Bearer ' + token
            }
        }).then(resp => {
            this.setState({list: resp.data});
        })
    }

    render() {
        const listItems = this.state.list.map(this.createdTasks)
        return (
            <div>
                <NavBar/>
                <section className="section">
                    <div className="container">
                        <h1 className="title">User List</h1>

                        <div className="columns">
                            <div className="column">

                            </div>
                            <div className="column is-three-fifths">
                                {listItems}
                            </div>
                            <div className="column">

                            </div>
                        </div>
                    </div>
                </section>
            </div>
        );
    }
}

export default ListUsers