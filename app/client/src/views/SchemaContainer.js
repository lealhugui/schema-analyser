import React, { Component } from 'react';
import { SchemaCard } from './Cards';
import JsonApiReq from '../Requests';

const BASE_URI = window.location.hostname;

class SchemaContainer extends Component{

  constructor (props) {
    super(props);
    this.state = {data: null};
    this.handleClickRebuild = this.handleClickRebuild.bind(this);
  }

  getCache() {
    let uri = BASE_URI+":8000";
    new JsonApiReq(uri, 'api/db_map_view/').get()
      .then((jsonData) => {
        if('success' in jsonData){
          if(jsonData.success===false){
            throw jsonData.err;
          }
        }
        this.setState({data: jsonData});
      })
      .catch((err) => {
        alert(err);
      });
  }

  handleClickRebuild() {

    let uri = BASE_URI+":8000";
    new JsonApiReq(uri, 'api/rebuild_db_map/').post()
      .then((jsonData) => {
         if('success' in jsonData){
          if(jsonData.success===false){
            throw jsonData.err;
          }
        }
        alert(JSON.stringify(jsonData));
      })
      .catch((err) => {
        alert(err);
      });

  }

  componentDidMount(){
  	this.getCache();
  }

  render() {
    let marginTop = {
      'marginTop': '5px'
    }
    console.log(this.props.location);
    return (
      <div>
        <div>
          <button onClick={this.handleClickRebuild} >Rebuild cache</button>
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

export default SchemaContainer;