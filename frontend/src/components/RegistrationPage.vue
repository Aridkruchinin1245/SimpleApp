<template>
    <div class="header">
        <h1>Регистрация</h1>
        <router-link to="/">На главную</router-link>
        <p>Уже есть аккаунт? <router-link to="/auth">Авторизация</router-link></p>
    </div>

    <div class="main">
        <form @submit.prevent="sendData">
            <p><input placeholder="логин" v-model="login"/></p>
            <p><input placeholder="возраст" v-model="age"/></p>
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

          auth.setToken(token)
          router.push('/')
        }
      catch(error){
        console.log(error)
       }
    }

</script>

<style>

</style>