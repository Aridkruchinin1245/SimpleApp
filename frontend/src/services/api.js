import axios from 'axios'

const API = axios.create({
  baseURL: process.env.VUE_APP_API_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
}
})
// запросы
API.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)
// ответы
API.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    return Promise.reject(error)
  }
)

export const postService = {
    async getAll() {
        const response = await API.get('/items')
        return response
    },
    async addPost(content, token) {
        const user_data = {'content':content}
        await API.post('/postCreate', user_data, {
      headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  })
    },
    async addLikes(id) {
        await API.get(`/addLike/${Number(id)}`)
    },
    async addDislikes(id) {
     await API.get(`/addDislike/${Number(id)}`)
    },
    async deleteData() {
        await API.post('/postDelete', {'command' : 'delete'})
    },
    async getAuthors() {
        const response = await API.get('/authors')
        return response
    },
    async getComments(id) {
        const response = await API.get(`/comments/${id}`)
        return response
    },
    async postComment(id, comment, token) {
      await API.post(`/comments/${Number(id)}`, {'comment':comment}, {
      headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }})
    },
    async postRegistration(login, age, password) {
      const response = await API.post('/reg', {'login':login, 'age':Number(age), 'password':password})
      return response
    },
    async getName(token) {
      const login = await API.post('/getName', {}, {
      headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  })
      return login
    },
    async sendAuthorisation(login, password) {
      const token = API.post('/auth', {'login':login, 'password':password})
      return token
    }
}