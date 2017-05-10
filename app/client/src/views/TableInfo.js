import React, { Component } from 'react';
import { Link } from 'react-router-dom';


class TableInfo extends Component {
	render(){
		return (
			<div>
				<p>#TODO: missing TableInfo Screen</p>
				<p>{this.props.match.params.name}</p>
				<Link to='/schemas'>Home</Link>
			</div>
		);
	}
}

export default TableInfo;