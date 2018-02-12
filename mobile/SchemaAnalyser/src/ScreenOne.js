import React, { Component } from 'react';
import {
  Platform,
  StyleSheet,
  Text,
  View,
  ScrollView
} from 'react-native';
import { Card, Button, ListItem } from 'react-native-elements';

export class ScreenOne extends Component<Props> {
  static navigationOptions = {
    title: "SCREEN ONE",
    header: null
  }

  constructor(props) {
    super(props);
    this.state = {
      objects: null

    };
  }

  async getDbMap() {
    try {
      const result = await fetch('http://172.22.4.98:8000/api/db_map_view/');
      const resultJSON = await result.json();
      return resultJSON;
    } catch (err) {
      alert(err);
    }
  } 

  componentDidMount() {
    this.getDbMap().then((jsonData) => {
      if('success' in jsonData){
        if(jsonData.success===false){
          throw jsonData.err;
        }
      }
      this.setState({objects: jsonData[0]});
    })
    .catch((err) => {
      alert(err);
    })    
  }

  render() {
    if(this.state.objects) {
      return (
        <View style={styles.container}>
          <ScrollView >
            {
              this.state.objects.tables.map((o, i) => {
                return (
                  <Card
                    key={i}
                    title={o.table_name}>
                    {
                      o.props.fields.map((f, idx) => {
                        return (
                          <Text
                            key={idx}>
                            {f.field_name}
                          </Text>
                        );
                      })
                    }
                  </Card>
                );
              })
            }
          </ScrollView>
        </View>
      );
    } else {
      return(
        <View style={styles.container}>
          <Text style={styles.instructions}>No Objects</Text>
        </View>
      );
    }
  }
    
}

const styles = StyleSheet.create({
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
    },
    instructions: {
      textAlign: 'center',
      color: '#333333',
      marginBottom: 5,
    },
});