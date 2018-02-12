import React from 'react';
import {
  StackNavigator,
} from 'react-navigation';

import { Home } from './src/Home';
import { ScreenOne } from './src/ScreenOne';

const RouterStack = StackNavigator({
  Home: { screen: Home },
  ScreenOne: { screen: ScreenOne}
},
{
  initialRouteName: 'Home'
});

export class App extends React.Component {
  render() {
    return <RouterStack />
  }
}