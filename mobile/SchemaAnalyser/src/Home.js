/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 * @flow
 */

import React, { Component } from 'react';
import {
  Platform,
  StyleSheet,
  Text,
  View
} from 'react-native';
import { Card, Button } from 'react-native-elements';

const instructions = Platform.select({
  ios: 'Press Cmd+R to reload,\n' +
    'Cmd+D or shake for dev menu',
  android: 'DOUBLE TAP R ON YOUR KEYBOARD TO RELOAD,\n' +
    'SHAKE OR PRESS MENU BUTTON FOR DEV MENU',
});

type Props = {};
export class Home extends Component<Props> {
  static navigationOptions = {
    title: "HOME",
    header: null
  }
  render() {
    return (
      <View style={styles.container}>
        <Card title='WELCOME TO REACT NATIVE!' style={styles.cardBlue}>
          <Text style={styles.instructions}>
            To get started, edit App.js
          </Text>
          <Button
              title="GO TO SCREENONE"
              icon={{name: 'code'}}
              backgroundColor='#03A9F4'
              onPress={()=>this.props.navigation.navigate('ScreenOne')}
              />
        </Card>
        <Card title='INSTRUCTIONS'>
          <Text style={styles.instructions}>
            {instructions}
          </Text>
        </Card>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  cardBlue: {
    color: '#4286F4',
  },
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'stretch',
    backgroundColor: '#F5FCFF',
  },
  welcome: {
    fontSize: 20,
    textAlign: 'center',
    margin: 10,
    color: '#4286F4'
  },
  instructions: {
    textAlign: 'center',
    color: '#333333',
    marginBottom: 5,
  },
});
