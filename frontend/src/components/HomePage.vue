
<template>
  <div>
    <h2>欢迎使用搜索系统喵</h2>
    <input
      v-model="query"
      placeholder="请输入搜索内容喵..."
      @keydown.enter="onSearch"
    />
    <select v-model="searchType" style="margin-left: 10px;">
      <option value="normal">普通搜索</option>
      <option value="phrase">短语搜索</option>
      <option value="wildcard">通配搜索</option>
    </select>
    <button @click="onSearch" style="margin-left: 10px;">搜索</button>

    <div v-if="searchLogs.length" class="search-logs">
      <h4>搜索历史</h4>
      <ul>
        <li
          v-for="(log, index) in searchLogs"
          :key="index"
          @click="useLog(log)"
          class="search-log-item"
        >
          {{ log.keyword }} （{{ log.type }}）
        </li>
      </ul>
      <button @click="clearLogs" class="clear-logs-btn">清除历史</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const query = ref('')
const searchType = ref('normal')
const router = useRouter()
const searchLogs = ref([])

const STORAGE_KEY = 'search_logs'

onMounted(() => {
  const logs = localStorage.getItem(STORAGE_KEY)
  if (logs) {
    searchLogs.value = JSON.parse(logs)
  }
})

function useLog(log) {
  query.value = log.keyword
  searchType.value = log.type
}

function saveLog(keyword, type) {
  // 新记录放最前面，去重
  searchLogs.value = searchLogs.value.filter(
    (item) => !(item.keyword === keyword && item.type === type)
  )
  searchLogs.value.unshift({ keyword, type })

  if (searchLogs.value.length > 10) {
    searchLogs.value.pop()
  }

  localStorage.setItem(STORAGE_KEY, JSON.stringify(searchLogs.value))
}

function clearLogs() {
  searchLogs.value = []
  localStorage.removeItem(STORAGE_KEY)
}

function onSearch() {
  if (query.value.trim()) {
    saveLog(query.value, searchType.value)
    router.push({ name: 'Search', query: { q: query.value, type: searchType.value } })
  }
}
</script>

<style scoped>
.search-logs {
  margin-top: 20px;
  max-width: 400px;
  font-size: 14px;
  color: #444;
}
.search-logs h4 {
  margin-bottom: 8px;
}
.search-log-item {
  cursor: pointer;
  padding: 4px 6px;
  border-bottom: 1px solid #eee;
}
.search-log-item:hover {
  background-color: #f0f0f0;
}
.clear-logs-btn {
  margin-top: 8px;
  font-size: 12px;
  background: #eee;
  border: none;
  padding: 4px 8px;
  cursor: pointer;
}
.clear-logs-btn:hover {
  background: #ddd;
}
</style>
