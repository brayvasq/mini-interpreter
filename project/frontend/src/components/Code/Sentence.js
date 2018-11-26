import React from 'react'
import './Sentence.css'
import axios from 'axios'

class Sentence extends React.Component {

    constructor(props) {
        super(props)

        this.state = {
            id: this.props.id,
            input_code: this.props.input,
            output_code: this.props.output
        }
        this.runSentence = this.runSentence.bind(this);
        this.removeSentence = this.removeSentence.bind(this);
        this.handleChangeInput = this.handleChangeInput.bind(this);
    }

    handleChangeInput(event) {
        this.setState({input_code: event.target.value})
    }

    runSentence(){
        //console.log(this.state)
        const token = localStorage.getItem("token");
        axios({
            method: 'put',
            url: 'http://localhost:8000/api/sentences/'+this.state.id,
            data:{
              input_code: this.state.input_code
            },
            headers: {
                Authorization: 'Bearer ' + token
            }
        }).then(resp => {
            //console.log(resp);
            this.setState({output_code: resp.data.output_code});
        })
    }

    removeSentence(){
        const token = localStorage.getItem("token");
        axios({
            method: 'delete',
            url: 'http://localhost:8000/api/sentences/'+this.state.id,
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
                    <div className="info-item">
                        <div className="field">
                            <div className="control">
                                <input className="input is-primary" type="text" placeholder="Primary input" value={this.state.input_code} onChange={this.handleChangeInput}/>
                            </div>
                        </div>
                    </div>
                    <div className="info-item">
                        <div className="control">
                            <input className="input" type="text" placeholder="Disabled input" value={this.state.output_code} disabled/>
                        </div>
                    </div>
                    <div className="info-item">
                        <div className="field has-addons">
                            <p className="control">
                                <a className="button is-success" onClick={this.runSentence}>
                                    <span className="icon is-small">
                                        <i className="far fa-play-circle"></i>
                                    </span>
                                    <span>Run</span>
                                </a>
                            </p>
                            <p className="control">
                                <a className="button is-danger" onClick={this.removeSentence}>
                                    <span className="icon is-small">
                                        <i className="far fa-trash-alt"></i>
                                    </span>
                                    <span>Delete</span>
                                </a>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default Sentence;