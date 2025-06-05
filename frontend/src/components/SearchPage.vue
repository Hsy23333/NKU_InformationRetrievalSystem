<!-- src/components/SearchPage.vue -->
<template>
  <div>
    <h2>搜索结果</h2>
    <p v-if="loading">加载中...</p>
    <ul v-else>
      <li v-for="item in results" :key="item.id">
        <h3>{{ item.title }}</h3>
        <p>{{ item.content }}</p>
        <a :href="item.url" target="_blank">{{ item.url }}</a>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const results = ref([])
const loading = ref(true)

onMounted(async () => {
  const query = route.query.q
  try {
    const res = await axios.get(`http://127.0.0.1:5000/search`, {
      params: { query: query }
    })
    results.value = res.data.results || []
  } catch (err) {
    console.error('搜索失败', err)
  } finally {
    loading.value = false
  }
})
</script>
