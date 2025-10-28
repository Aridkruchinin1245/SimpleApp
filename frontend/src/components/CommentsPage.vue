<template>
 <div class="header">
    <h1 class="logo">Комментарии к посту {{ id }}</h1>
    <nav class="nav">
     <router-link to="/">На главную</router-link> 
    </nav>
 </div>
 <div class="main">
   <div class="write_comment">
      <form @submit.prevent="addComment">
         <p><textarea rows="10" placeholder="Комментарий" v-model="comment"/></p>
         <p v-if="comment.length>10"><button type="submit">Отправить комментарий</button></p>
      </form>
   </div>
   <div v-if="comments">
      <div class="comment_space" v-for="comment in comments.data" :key="comment.id">
         <div class="post">
            <div class="timestamp">в: {{ comment.date }}</div>
            <div class="username">от: {{ comment.author }}</div>
            <div>{{ comment.content }}</div>
         </div>
      </div>
   </div>
   <div v-else>
      <div>Комментариев нет, напиши первым</div>
   </div>
 </div>
</template>

<script>
   import {ref, onMounted} from 'vue'
   import { postService } from '@/services/api';
   import { useRoute } from 'vue-router';
import { auth } from '@/utils/auth';

   export default {
      setup() {
         const route = useRoute()
         const id = route.params.id
         const comments = ref([])
         const comment = ref("")

         const showComments = async() => {
            comments.value = await postService.getComments(id)
         }
         const addComment = async() => {
            console.log(auth.getToken())
            await postService.postComment(id, comment.value, auth.getToken())
            comment.value = ''
            await showComments()
         }
         onMounted(showComments)
         
         return {showComments, comments, id, addComment, comment}
      }
   }
</script>

<style scoped>
   .comment_space {
      border:1px solid black;
      text-align: center;
      border-radius: 10px;
      padding: 10px;
      margin: 10px;
   }
   .main {
      text-align: center;
      padding: 10px;
   }
   .write_comment {
      text-align: center;
      padding: 10px;
   }
</style>
