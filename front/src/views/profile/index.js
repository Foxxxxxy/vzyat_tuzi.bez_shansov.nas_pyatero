import View from './view.vue'
import redirect_first from '../_middleware/redirect_first'

export default [
  {
    path: '/profile',
    name: 'Profile',
    component: View,
    meta: {
      middlewares: [redirect_first],
    },
  },
]
