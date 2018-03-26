import React from 'react';
import {TransitionGroup, CSSTransition} from 'react-transition-group';
import {
  Router,
  Route,
  Switch,
  Link
} from 'react-router-dom';
import logo from './molecule.svg';
import './App.css';
import SchemaContainer from './views/SchemaContainer';
import TableInfo from './views/TableInfo';
import TablesWithPks from './views/TablesWithPks';
//import JsonApiReq from './Requests';
import {
  API_URL,
  addLogoAnimation,
  removeLogoAnimation,
  handleErr } from './constants';
import createBrowserHistory from 'history/createBrowserHistory';
import $ from 'jquery';


/*
  Main app component and router
*/
const customHistory = createBrowserHistory();
const App = () => {

  const buildCache = function(e, h){
    e.preventDefault();
    const u = `http://${API_URL}/api/rebuild_db_map/`;
    addLogoAnimation();
    $.ajax({
      dataType: "json",
      url: u,
      success: (data) => {
        if("success" in data){
          if(data.success===false){
           handleErr(data);
           return;
          }
        }
        alert("Cache rebuilt!");
      },
      error: (e) => {
        console.log(e);
        alert(`${e}`);
      },
      complete: removeLogoAnimation
    })
  }

  return (
    <Router history={customHistory}>

        <div className="app">
          <div className="app-header">
            <div className="app-info">
              <div className="app-info element"><img id="app-logo" src={logo} className="rotating app-logo" alt="logo" /></div>
              <div className="app-info element"><h2 style={{height:"100%"}}>schema-analyser</h2></div>
            </div>
          </div>
          <div>
            <span>
              <nav className="navbar">
                <ul>
                  <li><Link to='/'>HOME</Link></li>
                  <li><Link to='/pks'>PK LIST</Link></li>
                  <li><a href="" onClick={buildCache} >REBUILD CACHE</a></li>
                </ul>

              </nav>
            </span>
            <div className="app-content">
              <TransitionGroup style={{height: '100%'}}
              className="rTransition"
              appear={true}
              timeout={500}>
                <Switch key={window.location.key}>
                  <Route location={window.location} exact path="/" component={SchemaContainer}/>
                  <Route location={window.location} path='/schemas' component={SchemaContainer} />
                  <Route location={window.location} path='/table/:name' component={TableInfo} />
                  <Route location={window.location} path='/pks' component={TablesWithPks} />
                </Switch>
              </TransitionGroup>
            </div>
          </div>



        </div>
    </Router>
  );
}

export default App;
