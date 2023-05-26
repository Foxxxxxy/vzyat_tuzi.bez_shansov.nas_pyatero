import View from './view.vue'
import redirect_first from '../_middleware/redirect_first'

export default [
  {
    path: '/buildings',
    name: 'Buildings',
    component: View,
    meta: {
      middlewares: [redirect_first],
    },
  },
]
