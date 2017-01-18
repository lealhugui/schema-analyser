import Relay from 'react-relay';

export default {
  viewer: Component => Relay.QL`
    query {
      User{
            ${Component.getFragment('viewer')}
        
      }
        
    }
  `
};
