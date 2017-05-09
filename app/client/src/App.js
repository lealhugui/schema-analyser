import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import { SchemaCard } from './Cards';
import JsonApiReq from './Requests';

const BASE_URI = window.location.hostname;

class App extends Component {

  constructor (props) {
    super(props);
    this.state = {data: null};
    this.handleClickRebuild = this.handleClickRebuild.bind(this);
    this.handleClickGet = this.handleClickGet.bind(this);
  }

  handleClickGet() {
    let uri = BASE_URI+":8000";
    new JsonApiReq(uri, 'api/db_map_view/').get()
      .then((jsonData) => {
        this.setState({data: jsonData});
      })
      .catch((a, b, c) => {
        alert(a);
      });
  }

  handleClickRebuild() {

    let uri = BASE_URI+":8000";
    new JsonApiReq(uri, 'api/rebuild_db_map/').post()
      .then((jsonData) => {
        alert(JSON.stringify(jsonData));
      })
      .catch((a, b, c) => {
        alert(a);
      });

  }

  render() {
    let marginTop = {
      'marginTop': '5px'
    }
    return (
      <div className="app">
        <div className="app-header">
          <img src={logo} className="app-logo" alt="logo" />
          <h2>schema-analyser</h2>
        </div>
        <div>
          <div className="app-intro">Aviable actions</div>
          <button onClick={this.handleClickRebuild} >Rebuild cache</button>
          <button onClick={this.handleClickGet} >Get cache</button>
        </div>
        <div>
          {this.state.data != null ? (
            <div>
              <SchemaCard schema={this.state.data[0]} />
            </div>
          ) : (
            <div style={marginTop}>No Schemas</div>
          )}
        </div>
      </div>
    );
  }
}

export default App;
