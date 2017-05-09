import React, { Component } from 'react';
import CSSTransitionGroup from 'react-transition-group/CSSTransitionGroup';
import {
  BrowserRouter as Router,
  Route,
  Switch
} from 'react-router-dom';
import logo from './logo.svg';
import './App.css';
import SchemaContainer from './views/SchemaContainer';
import TableInfo from './views/TableInfo';

class App extends Component {

  render() {
    return (
      <Router>
        <Route render={({location}) => (
          <div className="app">
            <div className="app-header">
              <img src={logo} className="app-logo" alt="logo" />
              <h2>schema-analyser</h2>
            </div>
            <div>
              <div className="app-intro">Welcome</div>
                <CSSTransitionGroup
                transitionName="example"
                transitionAppear={true}
                transitionAppearTimeout={500}
                transitionEnterTimeout={500}
                transitionLeaveTimeout={300}>
                  <Switch key={location.key}>
                    <Route location={location} exact path="/" component={SchemaContainer}/>
                    <Route location={location} path='/schemas' component={SchemaContainer} />
                    <Route location={location} path='/table/:name' component={TableInfo} />
                  </Switch>
                </CSSTransitionGroup>
            </div>

              
        
          </div>
        )} />
      </Router>
    );
  }
}

export default App;
