<template>
    <div class="header">
        <h1>Создание поста</h1>
        <router-link to="/">На главную</router-link>
    </div>

    <div class="main">
        <form @submit.prevent="sendData">
            <p><textarea rows="10" class="big_text" v-model="content" placeholder="Текст"/></p>
            <div v-if="content.length > 10">
                <p>
                    <button type="submit">
                    Подтвердить
                    </button>
                </p>  
            </div>
        </form>
    </div>

</template>

<script setup>

import { postService } from '@/services/api';
import { ref } from 'vue'
import { auth } from '@/utils/auth';

const content = ref("")

      async function sendData() {
      try {
          await postService.addPost(content.value, auth.getToken())
          content.value = ''
        }
      catch(error){
        console.log(error)
       }
    }
  
</script>

<style scoped>
    .header {
        text-align: center;
    }
    .main {
        text-align: center;
    }

</style>