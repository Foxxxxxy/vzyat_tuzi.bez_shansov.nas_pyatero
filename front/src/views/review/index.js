import View from './view.vue'
import redirect_first from '../_middleware/redirect_first'

export default [
  {
    path: '/review',
    name: 'Review',
    component: View,
    meta: {
      middlewares: [redirect_first],
    },
  },
]
