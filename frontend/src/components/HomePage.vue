<!-- src/components/HomePage.vue -->
<template>
  <div>
    <h2>欢迎使用搜索系统</h2>
    <input v-model="query" placeholder="请输入搜索内容..." />
    <button @click="onSearch">搜索</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const query = ref('')
const router = useRouter()

function onSearch() {
  if (query.value.trim()) {
    router.push({ name: 'Search', query: { q: query.value } })
  }
}
</script>
