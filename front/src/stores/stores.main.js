import { defineStore } from 'pinia'

export const useStore = defineStore('main', {
  state: () => ({
    user: {
      email: null,
      password: null,
      token: null,
      level: null,
      user_id: null,
      name: null
    },
    result: null
  }),
  actions: {},
})
