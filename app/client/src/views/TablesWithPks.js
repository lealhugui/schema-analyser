import React, { Component } from 'react';
/* import { Link } from 'react-router-dom'; */
import JsonApiReq from '../Requests';
import DynamicTable from '../DynamicTable';
import { API_URL } from '../constants';

class TablesWithPks extends Component{

    constructor(props){
        super(props);
        this.state = {};
    }

    componentDidMount(){
        new JsonApiReq(API_URL, 'api/table_pk_data/').get()
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

    render(){
        return (
            <DynamicTable data={this.state.data} />
        )
    }
}

export default TablesWithPks;