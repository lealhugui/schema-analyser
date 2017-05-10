import React, { Component } from 'react';
import CSSTransitionGroup from 'react-transition-group/CSSTransitionGroup';
import {
  BrowserRouter as Router,
  Route,
  Switch,
  Link
} from 'react-router-dom';
import logo from './logo.svg';
import './App.css';
import SchemaContainer from './views/SchemaContainer';
import TableInfo from './views/TableInfo';
import TablesWithPks from './views/TablesWithPks';
import JsonApiReq from './Requests';
import { API_URL } from './constants';
import createBrowserHistory from 'history/createBrowserHistory';

class App extends Component {
  
  constructor(){
    super();
    this.handleClickRebuild = this.handleClickRebuild.bind(this);
  }

  redirectAfterBuild(loc){
    loc.push("/");
  }

  handleClickRebuild(e, history) {
    e.preventDefault();
    let uri = API_URL;
    new JsonApiReq(uri, 'api/rebuild_db_map/').post()
      .then((jsonData) => {
         if('success' in jsonData){
          if(jsonData.success===false){
            throw jsonData.err;
          }
        }
        alert(JSON.stringify(jsonData));
        history.push('/');
      })
      .catch((err) => {
        alert(err);
      });

  }

  render() {
    const customHistory = createBrowserHistory();
    return (
      <Router history={customHistory}>
        <Route render={({ match, location, history }) => (
          <div className="app">
            <div className="app-header">
              <img src={logo} className="app-logo" alt="logo" />
              <h2>schema-analyser</h2>
            </div>
            <div>
              <div>
                <nav className="navbar">
                  <ul>
                    <li><Link to='/'>HOME</Link></li>
                    <li><Link to='/pks'>PK LIST</Link></li>
                    <li><a href="" onClick={(e) => {
                      this.handleClickRebuild(e, history)
                    }} >REBUILD CACHE</a></li>
                  </ul>
                  
                </nav>
              </div>

              <CSSTransitionGroup
              transitionName="rTransition"
              transitionAppear={true}
              transitionAppearTimeout={500}
              transitionEnterTimeout={500}
              transitionLeaveTimeout={300}>
                <Switch key={location.key}>
                  <Route location={location} exact path="/" component={SchemaContainer}/>
                  <Route location={location} path='/schemas' component={SchemaContainer} />
                  <Route location={location} path='/table/:name' component={TableInfo} />
                  <Route location={location} path='/pks' component={TablesWithPks} />
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
