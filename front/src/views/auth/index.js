import View from './view.vue';
import test_auth from '../_middleware/test_auth'

export default [
  {
    path: '/auth',
    name: 'Auth',
    meta: {
      layout: 'empty',
      middlewares: [],
    },
    component: View,
  },
];
