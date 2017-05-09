import React,  { Component } from 'react';
import './Cards.css';

export class TableCard extends Component{
    render(){
        let listWrapperStyles = {
            marginTop: '5px'
        }

        let flds = this.props.table.props.fields.map(
            (fld) => (
                <div key={fld.field_name} className="table-field " title={fld.field_name}>
                    {fld.field_name}<span className="fld-type">{fld.inner_type}</span>
                </div>
            )
        );

        return (
            <div className="table-card" title={this.props.table.table_name}>
                <span className="obj-identifier">[obj]</span>
                <b>{this.props.table.table_name}</b>
                <div style={listWrapperStyles}>{flds}</div>
            </div>
        );
    }
}

export class SchemaCard extends Component{

    render(){
        let listTables = (<div></div>);
        console.log(this.props)
        if (this.props.schema.tables !== null && this.props.schema.tables.length > 0)
        {
            listTables = this.props.schema.tables.map(
                (table) => <TableCard key={table.table_name} table={table} />
            )
        }
        return (
            <div className="schema-card">
                <div>
                    Schema Name: <b>{this.props.schema.schema_name}</b>
                </div>
                {listTables}
            </div>
        );
    }
}

