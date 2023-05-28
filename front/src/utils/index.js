export const getUserStatus = (level) => {
  return level === 3 ? 'Администратор' : 'Пользователь'
}
