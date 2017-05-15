import React from 'react';
import { Link } from 'react-router-dom';

/**
 *  @description: Dynamic simple table generator.  Recieves a JSON object list as parameter, and renders the objects as a html table.
 *  @param=data: The JSON array of objects. The component extpect the objects to have the same structure,
 *  so it uses the first object as "template" to render the others objects. The object can contain a propery
 *  named "_opt", wich should be an object, with the following properties:
 *
 *      links: an array of links that should be used to wrap each one of the columns. Must contain these 2 parameters:
 *          to: the href to follow
 *          columnName: the column to wrap
 *  
 *  @example
 *  ----
 *  [
 *      {
 *          "Header 1": "Foo",
 *          "Header 2": "Bar",
 *          "_opt": {
 *              "links": [{
 *                  "to": "/foo/bar"
 *                  "columnName": "Header 1"
 *              }]
 *              
 *          }
 *      },
 *      {
 *          "Header 1": "Lorem",
 *          "Header 2": "Ipsum",
 *          "_opt": {
 *              "links": [{
 *                  "to": "/lorem/ipsum"
 *                  "columnName": "Header 1"
 *              }]
 *              
 *          }
 *      }        
 *  ]
 *
 *   With this data, will be rendered a table with 2 columns, with the headers "Header 1" and "Header 2", with 2 rows, 
 *   and the first column of each row will be a link.
 *  @param styles: object with the reactjs styles. 
 */
export default (props) => {
    const d = props.data || [];
    let trList = [];
    let thead = []

    if(d.length===0){
        return (<div>Loading...</div>);
    }

    if(d.length>0){
        const r1 = d[0];
        let columNames = [];
        for(let k in r1){
            if (r1.hasOwnProperty(k) && typeof(r1[k])!=="object"){
                columNames.push(k);
            }
        }

        thead = columNames.map((c)=>          
            <td key={c}>{c}</td>
        );
        
        for(let i=0; i<d.length; i++){

            let tds = columNames.map( (c)=> {

                let result = (<td key={c}>{d[i][c]}</td>);
                
                if(d[i].hasOwnProperty("_opt")){
                    if(d[i]._opt.hasOwnProperty("links")){
                        for(let li=0; li<d[i]._opt.links.length; li++){   
                            if(d[i]._opt.links[li].columnName===c){
                                result = (
                                    <td key={c}>
                                        <Link to={d[i]._opt.links[li].to}>{d[i][c]}</Link>
                                    </td>
                                    );
                            }
                        }
                    }
                }
                return result;
            })
            trList.push(<tr key={i}>{tds}</tr>);
        }
    }

    return (
        <table 
            className={props.tbl_classes || "dyn-tbl"}
            style={props.tbl_styles} >
            <tbody>
                <tr className="thead">
                    {thead}
                </tr>
                {trList}
            </tbody>
        </table>    
    );

}