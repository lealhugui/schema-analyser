import React, { Component } from 'react';
/* import { Link } from 'react-router-dom'; */
import JsonApiReq from '../Requests';
import { AutoSizer, Grid } from 'react-virtualized';
import { API_URL } from '../constants';
import cn from 'classnames';

class TablesWithPks extends Component{

    constructor(props, context){
        super(props, context);
        this.columns = ["Table Name", "Primary Keys"];
        this.state = {
            data: [this.columns]
        };

        this._cellRenderer = this._cellRenderer.bind(this);
    }

    componentDidMount(){
        new JsonApiReq(API_URL, 'api/table_pk_data/').get()
            .then((jsonData) => {
                if('success' in jsonData){
                    if(jsonData.success===false){
                        throw jsonData.err;
                    }
                }
                let dataArr = [];
                dataArr.push(this.columns);
                for(let i=0; i<jsonData.length; i++){
                    let thisArr = []
                    for(let k in this.columns){
                        thisArr.push(jsonData[i][this.columns[k]]);
                    }
                    dataArr.push(thisArr.slice());
                }
                this.setState({data: dataArr.slice()});
            })
            .catch((err) => {
                alert(err);
            });
    }

    _cellRenderer ({ columnIndex, key, rowIndex, style }) {
        
        const rowClass = rowIndex % 2 === 0 ? styles.evenRow : styles.oddRow;

        let classNames = {
            ...rowClass,
            ...styles.cell
            
        }
        if(columnIndex>2){
            classNames = Object.assign(classNames, styles.centeredCell);
        }

        const list = this.state.data;        
        return (
            <div
            style={classNames}
            key={key}
            style={style}
            >
                {list[rowIndex][columnIndex]}
            </div>
        )  
    }


    render(){
        console.log(styles.BodyGrid);
        return (
            <div className="app-content">
            
                <AutoSizer >
                    {({ height, width }) => (

                        <Grid
                            cellRenderer={this._cellRenderer}
                            columnCount={this.state.data[0].length}
                            columnWidth={250}
                            height={height}
                            rowCount={this.state.data.length}
                            rowHeight={30}
                            width={width}
                            className="BodyGrid" />

                        )}
                    </AutoSizer> 
            </div>
        
             
        )
    }
}

const styles = {
    GridRow :{
        marginTop: '15px',
        display: 'flex',
        flexDirection: 'row',
    },
    GridColumn :{
        display: 'flex',
        flexDirection: 'column',
        flex: '1 1 auto',
    },
    LeftSideGridContainer :{
        flex: '0 0 50px',
    },
    BodyGrid :{
        width: '100%',
        border: '1px solid #e0e0e0',
    },
    evenRow :{
        borderBottom: '1px solid #e0e0e0',
    },
    oddRow :{
        backgroundColor: '#fafafa',
        borderBottom: '1px solid #e0e0e0',
    },
    headerCell :{
        width: '100%',
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        padding: '0 .5em',
        fontWeight: 'bold',
        borderRight: '1px solid #e0e0e0',
    },
    cell :{
        borderRight: '1px solid #e0e0e0',
        borderBottom: '1px solid #e0e0e0',
        width: '100%',
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        padding: '0 .5em',
    },
    centeredCell :{
        alignItems: 'center',
        textAlign: 'center',
    },
    letterCell :{
        fontSize: '1.5em',
        color: '#fff',
        textAlign: 'center',
    },
    noCells :{
        position: 'absolute',
        top: '0',
        bottom: '0',
        left: '0',
        right: '0',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: '1em',
        color: '#bdbdbd',
    }
};



export default TablesWithPks;