import { get_token } from '~/api/route.auth'
import { useStore } from '~/stores/stores.main'

export default async ({ to, from, next, redirect }) => {
  const isFirstTime = localStorage.getItem('popup_shown')

  if (!isFirstTime) {
    redirect('/auth')
  }
}
