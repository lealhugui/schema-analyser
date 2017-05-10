import React, { Component } from 'react';
import { SchemaCard } from './Cards';
import JsonApiReq from '../Requests';
import { API_URL } from '../constants';

class SchemaContainer extends Component{

  constructor (props) {
    super(props);
    this.state = {data: null};
    
  }

  getCache() {
    let uri = API_URL;
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

  componentDidMount(){
  	this.getCache();
  }

  render() {
    let marginTop = {
      'marginTop': '5px',
      marginLeft: 'auto',
      marginRight: 'auto'
    }
    return (
        <div>
          {this.state.data != null ? (
            <div>
              <SchemaCard schema={this.state.data[0]} />
            </div>
          ) : (
            <div style={marginTop}>No Schemas</div>
          )}
        </div>

    );
  }
}

export default SchemaContainer;