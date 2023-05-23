import { get_token } from '~/api/route.auth';
import { useStore } from '~/stores/stores.main';

export default async ({ to, from, next, redirect }) => {
  const store = useStore();

  const isFirstTime = localStorage.getItem('popup_shown');
  const user = localStorage.getItem('user')
    ? JSON.parse(localStorage.getItem('user'))
    : null;

  if (user) {
    const data = await get_token(user.email, user.password);
    if (data) {
      store.$state.user.email = user.email;
      store.$state.user.password = user.password;
      store.$state.user.level = user.level;
      store.$state.user.user_id = user.user_id;
      store.$state.user.token = user.token;
      localStorage.setItem('user', JSON.stringify(store.$state.user));
    } else {
      localStorage.removeItem('user');
      redirect('/auth');
    }
  }

  if (!isFirstTime && !user) {
    redirect('/auth');
  }

  return;
};
