import React from 'react';
import { Link } from 'react-router-dom';
import './Cards.css';

export const TableCard = (props) => {
    let listWrapperStyles = {
        marginTop: '5px'
    }
    let flds = null;
    if(typeof(props.table) !== 'undefined'){
        flds = props.table.props.fields.map(
            (fld) => (
                <div key={fld.field_name}
                     className="table-field "
                     title={fld.field_name}
                     style={{color: fld.is_primary_key===true ? 'red':'inherit'}} >
                    {fld.field_name}<span className="fld-type">{fld.inner_type}</span>
                </div>
            )
        );
    }
    else{
        return (<div>Ref Error</div>);
    }

    return (
        <div className="table-card" title={props.table.table_name}>
            <b>{props.table.table_name.toUpperCase()}</b>
            <span className="obj-identifier"><Link to={'/table/'+ props.table.table_name}>[obj]</Link></span>
            <div style={listWrapperStyles}>{flds}</div>
        </div>
    );
}

export const SchemaCard = (props) => {

    let listTables = (<div></div>);
    if (props.schema.tables !== null && props.schema.tables.length > 0)
    {
        listTables = props.schema.tables.map(
            (table) => <TableCard key={table.table_name} table={table} />
        )
    }
    return (
        <div className="schema-card">
            <div>
                Schema Name: <b>{props.schema.schema_name.toUpperCase()}</b>
            </div>
            {listTables}
        </div>
    );

}

