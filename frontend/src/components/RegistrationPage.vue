<template>
    <div class="header">
        <h1 class="logo">Регистрация</h1>
        <nav class="nav">
        <router-link to="/">На главную</router-link>
        <router-link to="/auth">Авторизация</router-link>
    </nav>
    </div>

    <div class="main">
        <form @submit.prevent="sendData" class="new-post">
            <p><input placeholder="логин" v-model="login"/></p>
            <p><input placeholder="возраст" v-model="age" type="number"/></p>
            <p><input placeholder="пароль" v-model="password"/></p>
            <p><button type="submit" @click="redirectToPage">Зарегистрироваться</button></p>
        </form>
    </div>
</template>

<script setup>
    import { postService } from '@/services/api';
    import { ref } from 'vue';
    import { useRouter } from 'vue-router';
    import { auth } from '@/utils/auth';

    const router = useRouter()
    
    const login = ref("")
    const age = ref("")
    const password = ref("")

    async function sendData() {
      try {
          const data = await postService.postRegistration(login.value, age.value, password.value)
          login.value = ''
          age.value = ''
          password.value = ''

          console.log(data)

          const token = data.token

          try {
            auth.setToken(token)
            router.push('/')
          }
          catch (error) {
            alert(error)
          }

    }
      catch(error){
        alert(error)
       }
    }

</script>

<style>

</style>