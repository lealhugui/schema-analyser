import React, { Component } from 'react';
import JsonApiReq from '../Requests';
import { 
    API_URL, 
    removeLogoAnimation, 
    addLogoAnimation } from '../constants';
import DynamicTable from '../DynamicTable';

/**
 * @description View that shows a grid with the tables with their PKs
 */
class TablesWithPks extends Component{

    constructor(props){
        super(props);
        this.columns = ["Table Name", "Primary Keys"];
        this.state = {
            data: []
        };
    }

    componentDidMount(){
        addLogoAnimation();

        new JsonApiReq(API_URL, 'api/table_pk_data/').get()
            .then((jsonData) => {
                if('success' in jsonData){
                    if(jsonData.success===false){
                        throw jsonData.err;
                    }
                }
                let thisData = [];
                for(let i=0; i<jsonData.length; i++){
                    thisData.push({
                        "Table Name": jsonData[i]["Table Name"].toUpperCase(),
                        "Primary Keys": jsonData[i]["Primary Keys"],
                        "_opt": {
                            links: [{
                                to: "/table/"+jsonData[i]["Table Name"],
                                columnName: "Table Name"
                            }]
                        }
                    });
                }
                this.setState({data: thisData});
            })
            .catch((err) => {
                alert(err);
            });
            removeLogoAnimation();
    }


    render(){
        return (
            <div>
                <span><h2>Tables And Primary Keys</h2></span>
                <DynamicTable data={this.state.data} />
            </div>
             
        )
    }
}
export default TablesWithPks;