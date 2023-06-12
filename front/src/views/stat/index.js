import View from './view.vue'
import redirect_first from '../_middleware/redirect_first'

export default [
  {
    path: '/stat',
    name: 'Stat',
    component: View,
    meta: {
      middlewares: [redirect_first],
    },
  },
]
