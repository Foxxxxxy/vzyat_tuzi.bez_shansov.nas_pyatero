import { get_token } from '~/api/route.auth';
import { useStore } from '~/stores/stores.main';

export default async ({ to, from, next, redirect }) => {
  const store = useStore();

  const isFirstTime = localStorage.getItem('popup_shown');

  if (!isFirstTime) {
    redirect('/auth');
  }

  if (from.path === '/auth') {
    return
  }

  const user = localStorage.getItem('user')
    ? JSON.parse(localStorage.getItem('user'))
    : null;
  if (!user) return;
  const tokenData = await get_token(user.email, user.password);
  if (tokenData.status !== 'error') {
    store.$state.user.email = tokenData.email;
    store.$state.user.password = tokenData.password;
    store.$state.user.level = tokenData.level;
    store.$state.user.user_id = tokenData.user_id;
    store.$state.user.token = tokenData.access_token;
  }
};
