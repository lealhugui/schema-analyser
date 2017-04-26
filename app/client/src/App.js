import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import { SchemaCard } from './Cards';
import JsonApiReq from './Requests';

class App extends Component {

  constructor (props) {
    super(props);
    this.state = {data: null};
    this.handleClickRebuild = this.handleClickRebuild.bind(this);
    this.handleClickGet = this.handleClickGet.bind(this);
  }

  handleClickGet() {
    let uri = window.location.hostname+":8000";
    new JsonApiReq(uri, 'api/db_map_view/').get()
      .then((jsonData) => {
        this.setState({data: jsonData});
      });
  }

  handleClickRebuild() {

    let uri = window.location.hostname+":8000";
    new JsonApiReq(uri, 'api/rebuild_db_map/').post()
      .then((jsonData) => {
        alert(JSON.stringify(jsonData));
      });

  }

  render() {
    return (
      <div className="App">
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2>Welcome to React</h2>
        </div>
        <p className="App-intro">
          To get started, edit <code>src/App.js</code> and save to reload.
        </p>
        <button onClick={this.handleClickRebuild} >Rebuild cache</button>
        <button onClick={this.handleClickGet} >Get cache</button>
        <div>
          {this.state.data != null ? (
            <div>
              <SchemaCard schema={this.state.data[0]} />
            </div>
          ) : (
            <div >No Schemas</div>
          )}
        </div>
      </div>
    );
  }
}

export default App;
