<template>
  <div class="search-container">
    <h2>搜索结果</h2>
    <p v-if="loading" class="loading-text">加载中...</p>
    <p v-else-if="results.length === 0" class="no-results">暂无结果</p>
    <ul v-else class="results-list">
      <li v-for="item in results" :key="item.url" class="result-item">
        <h3 class="result-title">
          <a :href="item.url" target="_blank" rel="noopener noreferrer">
            {{ item.title || '无标题' }}
          </a>
        </h3>
        <p class="result-content">{{ truncateText(item.content) }}</p>
        <a :href="item.url" target="_blank" class="result-link" rel="noopener noreferrer">
          {{ item.url }}
        </a>
        <button
          v-if="item.snapshot_filename"
          class="snapshot-button"
          @click="openSnapshot(item)"
          type="button"
        >
          网页快照
        </button>
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

const query = route.query.q || ''
const searchType = route.query.type || 'normal'
const prefs = route.query.prefs || ''

function truncateText(text = '', maxLength = 150) {
  if (text.length <= maxLength) return text
  return text.slice(0, maxLength) + '...'
}

function openSnapshot(item) {
  const path = `http://localhost:5000/snapshots/${item.snapshot_filename}`
  window.open(path, '_blank')
}

onMounted(async () => {
  try {
    const res = await axios.post('http://127.0.0.1:5000/search', {
      keyword: query,
      type: searchType,
      prefs: prefs
    })
    results.value = res.data || []
  } catch (err) {
    console.error('搜索失败', err)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.search-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  color: #333;
}

.loading-text,
.no-results {
  font-size: 16px;
  color: #666;
  text-align: center;
  margin-top: 20px;
}

.results-list {
  list-style: none;
  padding: 0;
  margin-top: 20px;
}

.result-item {
  border-bottom: 1px solid #eee;
  padding: 15px 0;
}

.result-title {
  font-size: 20px;
  margin: 0 0 8px 0;
}

.result-title a {
  color: #007acc;
  text-decoration: none;
}

.result-title a:hover {
  text-decoration: underline;
}

.result-content {
  font-size: 14px;
  color: #555;
  margin: 0 0 10px 0;
  white-space: normal;
  word-break: break-word;
}

.result-link {
  font-size: 13px;
  color: #1a0dab;
  text-decoration: none;
  word-break: break-all;
}

.result-link:hover {
  text-decoration: underline;
  cursor: pointer;
}

.snapshot-button {
  margin-top: 8px;
  padding: 6px 12px;
  font-size: 13px;
  background-color: #007acc;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  user-select: none;
  transition: background-color 0.3s ease;
}

.snapshot-button:hover {
  background-color: #005f99;
}
</style>
