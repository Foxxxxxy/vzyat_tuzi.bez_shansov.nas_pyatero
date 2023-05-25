import { useStore } from '~/stores/stores.main'

export default async ({ to, from, next, redirect }) => {
  const store = useStore()

  const isFirstTime = localStorage.getItem('popup_shown')
  const user = (localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')) : null)

  if (user) {
    store.$state.user.email = user.email
    store.$state.user.password = user.password
    store.$state.user.level = user.level
    store.$state.user.user_id = user.user_id
    store.$state.user.token = user.token
    redirect('/')
  }
}
