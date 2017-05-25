import React from 'react';
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
import {
  API_URL,
  addLogoAnimation,
  removeLogoAnimation } from './constants';
import createBrowserHistory from 'history/createBrowserHistory';

/*
  Main app component and router
*/
const App = () => {

  const handleClickRebuild = (e, history) => {
    e.preventDefault();
    addLogoAnimation();
    new JsonApiReq(API_URL, "api/rebuild_db_map/").post()
      .then((jsonData) => {
         if("success" in jsonData){
          if(jsonData.success===false){
            throw jsonData.err;
          }
        }
        history.push("/");
      })
      .catch((err) => {
        alert(err);
      })
      .then(removeLogoAnimation);

  }

  const customHistory = createBrowserHistory();
  return (
    <Router history={customHistory}>

        <div className="app">
          <div className="app-header">
            <div className="app-info">
              <div className="app-info element"><img id="app-logo" src={logo} className="app-logo" alt="logo" /></div>
              <div className="app-info element"><h2 style={{height:"100%"}}>schema-analyser</h2></div>
            </div>
          </div>
          <div>
            <span>
              <nav className="navbar">
                <ul>
                  <li><Link to='/'>HOME</Link></li>
                  <li><Link to='/pks'>PK LIST</Link></li>
                  <li><a href="" onClick={(e) => {
                    handleClickRebuild(e, history)
                  }} >REBUILD CACHE</a></li>
                </ul>

              </nav>
            </span>
            <div className="app-content">
              <CSSTransitionGroup style={{height: '100%'}}
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



        </div>
    </Router>
  );
}

export default App;
