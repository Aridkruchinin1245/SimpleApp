<!-- <template>
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
</template> -->

<script>
  import {ref, onMounted} from 'vue';
  import { postService } from '@/services/api';
  import { auth } from '@/utils/auth';
  // import { useRouter } from 'vue-router';


  export default {
    setup() {

      // const router = useRouter()
      const items = ref([])
      const login = ref("")
      const content = ref("")

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
      const sendPost = async() => {
          if (auth.getToken()) {
          await postService.addPost(content.value, auth.getToken())
          content.value = ''
          fetchItems() 
        }
        else {
          alert('Зарегистрируйся для отправки поста')
        }
      }
      
      onMounted(fetchItems)
      return {items, addLike, addDislike, fetchItems, clearDatabase, login,
         leave, sendPost, content}
      
    }
  }
</script>

<!-- <style scoped>
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
</style> -->

<template>
  <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nuclear Forum</title>
</head>
<body>
    <div class="container">
        <header class="header">
            <div class="logo">NUCLEAR FORUM</div>
            <nav class="nav">
                <router-link :to="`/user/${login}`" v-if="login">{{ login }}</router-link>
                <router-link to="/">Главная</router-link>
                <router-link to="/auth">Авторизация</router-link>
                <router-link to="/reg">Регистрация</router-link>
                <router-link to="/weather">Погода</router-link>
                <a href="#">Сообщества</a>
                <a href="#">Поиск убежищ</a>
            </nav>
        </header>

        <div class="new-post">
            <form @submit.prevent="sendPost()">
              <textarea v-model="content" placeholder="Поделитесь своими находками в пустошах... (от 10 символов, не засорять эфир)"></textarea>
              <button v-if="content.length>10" type="submit">Опубликовать</button>
            </form>
        </div>

        <div class="main-content">
            <div class="posts">
                <div class="post" v-for="item in items" :key="item.id">
                    <div class="post-header">
                        <span class="username">{{ item.author }}</span>
                        <span class="timestamp">{{ item.date }}</span>
                    </div>
                    <div class="post-content">
                        {{ item.content }}
                    </div>
                    <div class="post-actions">
                      <nav class="nav">
                        <button @click="addLike(item.id)">▲ {{ item.likes }}</button>
                        <button @click="addDislike(item.id)">▼ {{ item.dislikes }}</button>
                        <router-link :to="`/comments/${item.id}`">Комментировать</router-link>
                    </nav>
                  </div>
                </div>
            </div>

            <aside class="sidebar">
                <!-- <div class="online-users">
                    <h3>Наши сталкеры</h3>
                    <div class="user">
                        <div class="status-dot"></div>
                        <span>Raider_Killer</span>
                    </div>
                </div> -->

                <div class="community-rules">
                    <h3>Правила выживания</h3>
                    <ul>
                        <li>Делитесь только проверенной информацией</li>
                        <li>Не раскрывайте координаты убежищ</li>
                        <li>Помогайте новичкам ориентироваться</li>
                        <li>Сообщайте об опасных зонах</li>
                    </ul>
                </div>
            </aside>
        </div>

        <footer class="footer">
            <p>Nuclear Forum © 2024 | Связь через ретрансляторы | Выживаем вместе</p>
        </footer>
    </div>
</body>
</html>
</template>

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background-color: #1a1a1a;
            color: #ffd700;
            font-family: Arial, sans-serif;
            line-height: 1.6;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            background: linear-gradient(135deg, #ffcc00, #e69500);
            padding: 20px;
            border-radius: 2px;
            margin-bottom: 20px;
            border: 1px solid #ff6600;
            box-shadow: 0 2px 4px rgba(255, 204, 0, 0.3);
        }

        .logo {
            font-size: 2.5em;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
            margin-bottom: 10px;
            color: #2a2a2a;
        }

        .nav {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }

        .nav a {
            color: #2a2a2a;
            text-decoration: none;
            padding: 8px 16px;
            background: #ffcc00;
            border-radius: 1px;
            border: 1px solid #ff9900;
            font-weight: bold;
            transition: all 0.3s ease;
        }

        .nav a:hover {
            background: #ff9900;
            transform: translateY(-1px);
        }

        .main-content {
            display: grid;
            grid-template-columns: 1fr 300px;
            gap: 20px;
        }

        .posts {
            background: #2a2a2a;
            border-radius: 2px;
            padding: 20px;
            border: 1px solid #ffcc00;
        }

        .post {
            background: #333333;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 1px;
            border-left: 3px solid #ffcc00;
            border-bottom: 1px solid #444444;
        }

        .post-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 1px solid #444444;
        }

        .username {
            color: #ffaa00;
            font-weight: bold;
            font-size: 1.1em;
        }

        .timestamp {
            color: #ffcc00;
            font-size: 0.9em;
            opacity: 0.8;
        }

        .post-content {
            margin-bottom: 12px;
            color: #eeeeee;
            line-height: 1.5;
        }

        .post-actions {
            display: flex;
            gap: 12px;
        }

        .post-actions button {
            background: #ffcc00;
            border: none;
            padding: 6px 12px;
            border-radius: 1px;
            cursor: pointer;
            color: #2a2a2a;
            font-weight: bold;
            transition: all 0.2s ease;
        }

        .post-actions button:hover {
            background: #ffaa00;
        }

        .sidebar {
            background: #2a2a2a;
            border-radius: 2px;
            padding: 20px;
            border: 1px solid #ffcc00;
        }

        .sidebar h3 {
            color: #ffaa00;
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 1px solid #444444;
        }

        .online-users {
            margin-bottom: 25px;
        }

        .user {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 8px;
            border-bottom: 1px solid #444444;
            transition: background-color 0.2s ease;
        }

        .user:hover {
            background: #333333;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background: #00cc00;
            border-radius: 1px;
        }

        .new-post {
            background: #2a2a2a;
            padding: 20px;
            border-radius: 2px;
            margin-bottom: 20px;
            border: 1px solid #ffcc00;
        }

        .new-post textarea {
            width: 100%;
            height: 100px;
            background: #333333;
            border: 1px solid #ffcc00;
            border-radius: 1px;
            padding: 12px;
            color: #eeeeee;
            margin-bottom: 12px;
            resize: vertical;
            font-family: Arial, sans-serif;
        }

        .new-post textarea:focus {
            outline: none;
            border-color: #ffaa00;
            box-shadow: 0 0 5px rgba(255, 204, 0, 0.5);
        }

        .new-post button {
            background: #ffcc00;
            color: #2a2a2a;
            border: none;
            padding: 10px 20px;
            border-radius: 1px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s ease;
        }

        .new-post button:hover {
            background: #ffaa00;
            transform: translateY(-1px);
        }

        .community-rules ul {
            list-style: none;
            padding-left: 0;
        }

        .community-rules li {
            padding: 8px 0;
            border-bottom: 1px solid #444444;
            color: #dddddd;
        }

        .community-rules li:before {
            content: "▸";
            color: #ffcc00;
            margin-right: 8px;
        }

        .footer {
            text-align: center;
            margin-top: 20px;
            padding: 20px;
            color: #ffcc00;
            border-top: 1px solid #ffcc00;
            background: #2a2a2a;
            border-radius: 2px;
        }

          input {
            width: 100%;
            height: 15px;
            background: #333333;
            border: 1px solid #ffcc00;
            border-radius: 1px;
            padding: 12px;
            color: #eeeeee;
            margin-bottom: 12px;
            resize: vertical;
            font-family: Arial, sans-serif;
        }

        textarea {
            width: 100%;
            background: #333333;
            border: 1px solid #ffcc00;
            border-radius: 1px;
            padding: 12px;
            color: #eeeeee;
            margin-bottom: 12px;
            resize: vertical;
            font-family: Arial, sans-serif;
        }

        

        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
            }
            
            .nav {
                justify-content: center;
            }
        }
    </style>