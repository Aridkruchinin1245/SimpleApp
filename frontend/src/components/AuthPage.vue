<template>
     <div class="header">
        <h1>Авторизация</h1>
        <router-link to="/">На главную</router-link>
    </div>

    <div class="main">
        <form @submit="authorisation">
            <p><input v-model="login" placeholder="Логин"/></p>
            <p><input v-model="password" placeholder="Пароль"/></p>
            <p><button type="submit">Авторизоваться</button></p>
        </form>
    </div>
</template>

<script setup>
    import { postService } from '@/services/api';
    import { ref } from 'vue';
    // import { useRouter } from 'vue-router';
    import { auth } from '@/utils/auth';

    const login = ref("")
    const password = ref("")

    // const router = useRouter()

    async function authorisation() {
        try {
            const response = await postService.sendAuthorisation(login.value, password.value)
            auth.setToken(response)
            console.log(response)
            // router.push('/')
        }
        catch (error) {
            alert('Аккаунт не найден')
        }
    }

</script>

<style>

</style>