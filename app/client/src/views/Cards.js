import React,  { Component } from 'react';
import { Link } from 'react-router-dom';
import './Cards.css';

export class TableCard extends Component{
    render(){
        let listWrapperStyles = {
            marginTop: '5px'
        }

        let minLink = {
            fontSize: "x-small"
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
                <b>{this.props.table.table_name}</b>
                <span className="obj-identifier">[obj]</span>
                <div style={listWrapperStyles}>{flds}</div>
                <div style={minLink}><Link to={'/table/'+ this.props.table.table_name}>mais informações</Link></div>
            </div>
        );
    }
}

export class SchemaCard extends Component{

    render(){
        let listTables = (<div></div>);
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

