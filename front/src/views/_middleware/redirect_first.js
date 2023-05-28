import { get_token } from '~/api/route.auth';
import { get_user_info } from '~/api/route.user'
import { useStore } from '~/stores/stores.main';

export default async ({ to, from, next, redirect }) => {
  const store = useStore();

  const isFirstTime = localStorage.getItem('popup_shown');

  if (!isFirstTime) {
    redirect('/auth');
  }

  const user = localStorage.getItem('user')
    ? JSON.parse(localStorage.getItem('user'))
    : null;
  if (!user) return
  const tokenData = await get_token(user.email, user.password)
  if (tokenData.status !== 'error') {
    store.$state.user.email = tokenData.email;
    store.$state.user.password = tokenData.password;
    store.$state.user.level = tokenData.level;
    store.$state.user.user_id = tokenData.user_id;
    store.$state.user.token = tokenData.token;
  } else {
    localStorage.removeItem('user')
  }
  const data = await get_user_info(store.$state.user.token);
  if (data.status !== 'error') {
    store.$state.user.name = data.name;
  }
};
