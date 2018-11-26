import React from 'react';
import NavBar from '../NavBar/NavBar'
import axios from 'axios'
import './Code.css'
import Sentence from './Sentence'

class Code extends React.Component{

    constructor(props){
        super(props)

        this.state = {
            list: []
        };

        this.getCode = this.getCode.bind(this);
    }

    componentDidMount() {
        setInterval(this.getCode,2000)
        //this.getCode()
    }

    createdCodes(item) {
        return <Sentence key={item.id} id={item.id} input={item.input_code} output={item.output_code}></Sentence>
    }

    getCode(){
        const token = localStorage.getItem("token");
        axios({
            method: 'get',
            url: 'http://localhost:8000/api/sentences',
            headers: {
                Authorization: 'Bearer ' + token
            }
        }).then(resp => {
            //console.log(resp);
            this.setState({list: resp.data});
        })
    }

    render(){
        const listItems = this.state.list.map(this.createdCodes)
        return(
            <div>
                <NavBar create={true}/>
                <section className="section">
                    <div className="container">
                        <h1 className="title">Sentences List</h1>

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

export default Code;