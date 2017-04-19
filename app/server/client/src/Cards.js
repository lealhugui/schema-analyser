import React,  { Component } from 'react';
import './Cards.css';

export class TableCard extends Component{
    render(){
        return (
            <div className="Table-card">
                Table Name: {this.props.table_name} 
            </div>
        );
    }
}

export class SchemaCard extends Component{

    render(){
        let listTables = (<div></div>);
        if (this.props.schema.tables != null && this.props.schema.tables.length > 0)
        {
            listTables = this.props.schema.tables.map(
                (table) => <TableCard table_name={table.name} />
            )
        }
        return (
            <div className="Schema-card">
                Schema Name: {this.props.schema.name}
                {listTables}
            </div>
        );
    }
}

