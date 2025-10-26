<template>
  <div class="header">
    <h1 class="bright">Simple app</h1>
    <div>
      <span class="h-el" v-if="login != 'Зарегистрируйся'">
        <router-link to="/user/">{{ login }}</router-link>
      </span>
        <div v-else>
        <span class="h-el">{{ login }}</span>
        </div>
      <button class="h-el" @click="leave()">Выйти</button>
      <span class="h-el"><router-link to="/auth">Авторизация</router-link></span>
      <span class="h-el"><router-link to="/reg">Регистрация</router-link></span>
      <span class="h-el"><router-link to="/postCreate">Создание поста</router-link></span>
      <span class="h-el"><button @click.prevent="clearDatabase()">Очистить посты</button></span>
    </div>
  </div>

  <div class="main">
    <div v-for="item in items" :key="item.id" class="post">

        <p class="author">Автор: {{item.author}}</p>
        <p class="date">{{item.date}}</p>
        <p>{{item.content}}</p>

        <div class="likebar">
          <span>{{item.likes}}</span>
          <button @click="addLike(item.id)"><img src="/like.png"/></button>

          <span>{{item.dislikes }}</span>
          <button @click="addDislike(item.id)"><img src="/dislike.png"/></button>

          <span></span>
          <router-link :to="`/comments/${item.id}`"><button ><img src="/comment.png"/></button></router-link>
        </div>
    </div>
  </div>

  <div class="footer">
    <div><router-link to="authors">Авторы постов</router-link></div>
    <div>@Aridkruchinin1245</div>
  </div>
</template>

<script>
  import {ref, onMounted} from 'vue';
  import { postService } from '@/services/api';
  import { auth } from '@/utils/auth';
  // import { useRouter } from 'vue-router';


  export default {
    setup() {

      // const router = useRouter()
      const items = ref([])
      const login = ref("Зарегистрируйся")
      const fetchItems = async() => {
        try {
          const response = await postService.getAll()
          items.value = response.data
          const token = auth.getToken()

          if (token) {
            login.value = await postService.getName(token)
            console.log(login)
            console.log('авторизован')
          }
          else {
            // router.push('/reg')
            alert('Зарегистрируйтесь для полноценной работы')
            console.log('неавторизован')
          }
         }
        catch(error) {
          console.log(error)
        }
    }

       const addLike = async (id) => {
        await postService.addLikes(id)
        await fetchItems() 
      }
      const addDislike = async (id) => {
        await postService.addDislikes(id)
        await fetchItems() 
        
      }
      const clearDatabase = async() => {
        await postService.deleteData()
        await fetchItems()
      }
      const leave = async() => {
        auth.removeToken()
      }
      
      onMounted(fetchItems)
      return {items, addLike, addDislike, fetchItems, clearDatabase, login, leave}
      
    }
  }
</script>

<style scoped>
    .bright {
      color: blue;
      font-size: large;
    }
    .main {
      text-align: center;
      display: flex;
      flex-direction: column;
      min-height: 75vh; 
    }
    .footer {
      text-align: center;
    }
    .header {
      text-align: center;
    }
    .post {
      border:1px solid black;
      border-radius: 10px;
      padding: 10px;
      margin: 10px;
    }
    .author {
      text-align: start;
      color: darkgrey;
    }
    .date {
      text-align: start;
      color: darkgrey;
      font-size: 8pt;
    }
    img {
      width: 20px;
      height: 20px;
    }
    .likebar {
      text-align: end;
    }
    .h-el {
      margin: 10px;
    }
</style>