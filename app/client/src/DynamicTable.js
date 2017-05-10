import React, { Component } from 'react';

class DynamicTable extends Component {
    render(){
        const d = this.props.data || [];
        let trList = [];
        let ths = []

        if(d.length>0){
            const r1 = d[0];
            let columNames = [];
            for(let k in r1){
                if (r1.hasOwnProperty(k) && typeof(r1[k])!=="object"){
                    columNames.push(k);
                }
            }

            columNames.sort(function(a,b) {
                let x = a.toLowerCase();
                let y = b.toLowerCase();
                return x > y ? -1 : x < y ? 1 : 0;
            });

            ths = columNames.map((c)=>
                <th key={c}>{c}</th>
            );
            
            for(let i=0; i<d.length; i++){
                let tds = columNames.map((c)=>
                    <td key={c}>{d[i][c]}</td>
                )
                trList.push(<tr key={i}>{tds}</tr>);
            }
        }
    
        return (
            <table 
                className={this.props.tbl_classes || "dyn-tbl"}
                style={this.tbl_styles} >
                <thead>
                    <tr>
                        {ths}
                    </tr>
                </thead>
                <tbody>            
                    {trList}
                </tbody>
            </table>    
        );

    }
}

export default DynamicTable;