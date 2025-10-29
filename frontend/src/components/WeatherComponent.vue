<template>
    <div class="header">
        <div class="logo">Погода</div>
        <nav class="nav">
            <router-link to="/">На главную</router-link>
        </nav>
    </div>
    <div class="main">
        <div class="new-post">
            <div>* не работает без подключения к интернету</div>
            <form @submit.prevent="get_weather(`${city}`)">
                <input type="text" v-model="city">
                <button type="submit">Узнать</button>
            </form>
        </div>
    <div class="post" v-if="weather">
        <div>В {{city}} {{ weather.description }}</div>
        <div>Температура {{ weather.temp }}°C</div>
        <div>Ветер {{ weather.wind }} м/с</div>
    </div>

    </div>
</template>

<script setup>
    import { ref } from 'vue'
    import { postService } from '@/services/api';

    const city = ref("")
    const weather = ref("")

    async function get_weather(data) {
        try {weather.value = await postService.get_weather(data)
            return weather
        }
        catch {
            alert('Город не найден')
        }
    }

</script>