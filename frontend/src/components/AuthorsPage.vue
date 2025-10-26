<template>
    <div class="header">
        <h1>Авторы постов</h1>
        <router-link to="/">На главную</router-link>
    </div>
    <div class="main">
        <div v-if="authors">
        <div class="authors" v-for="(author, index) in authors" :key="index">
            <li class="author">{{author}}</li>
        </div>
        </div>
        <div v-else>
            <li>Авторов нет, стань первым</li>
        </div>
    </div>
</template>

<script>
    import { postService } from '@/services/api';
    import { ref, onMounted } from 'vue';

    export default {
        setup() {
            const authors = ref([]) 

            const authors_get = async() => {
                const response = await postService.getAuthors()
                authors.value = response.data
            }
            
            onMounted(authors_get)
            console.log(authors.value)
            return {authors}
    }
}

</script>

<style>
    .header {
        text-align: center;
    }
    .main {
        text-align: center;
    }
    .authors {
        text-align: center;
    }
    .author {
        font-size: large;
        color: blue;
    }
</style>