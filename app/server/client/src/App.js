import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import { SchemaCard } from './Cards';

class App extends Component {

  constructor (props) {
    super(props);
    this.state = {data: null};
    this.handleClickRebuild = this.handleClickRebuild.bind(this);
    this.handleClickGet = this.handleClickGet.bind(this);
  }

  handleClickGet() {
    let opt = {
      method: 'GET',
      headers: new Headers(),
      mode: 'cors',
      cache: 'default'
    };
    let req = new Request('api/db_map_view/', opt);

    fetch(req).then((response) => {
      return response.json();
    }).then((jsonData) => {
      alert(JSON.stringify(jsonData))
      this.setState({data: jsonData});
    })    
  }

  handleClickRebuild() {
    let opt = {
      method: 'POST',
      headers: new Headers(),
      mode: 'cors',
      cache: 'default'
    };
    let req = new Request('api/rebuild_db_map/', opt);

    fetch(req).then((response) => {
      return response.text();
    }).then((txt) => {
      alert(txt);
    })
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
