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

    <div class="history-and-preferences">
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

      <div class="preferences">
        <h4>偏好选择</h4>
        <div class="checkbox-group">
          <label v-for="item in sourceTypes" :key="item.value" class="checkbox-label">
            <input type="checkbox" :value="item.value" v-model="selectedSourceTypes" />
            {{ item.label }}
          </label>
        </div>
      </div>
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

const sourceTypes = [
  { value: '12club', label: '动漫' },
  { value: 'ai', label: '人智' },
  { value: 'bs', label: '商学' },
  { value: 'cc', label: '计算机' },
  { value: 'ceo', label: '电光' },
  { value: 'chem', label: '化学' },
  { value: 'cs', label: '软件' },
  { value: 'cyber', label: '网安' },
  { value: 'cz', label: '马克思' },
  { value: 'env', label: '环科' },
  { value: 'finance', label: '金融' },
  { value: 'graduate', label: '研究生' },
  { value: 'history', label: '历史' },
  { value: 'hyxy', label: '汉语言' },
  { value: 'jc', label: '新传' },
  { value: 'jwcold', label: '教务处' },
  { value: 'law', label: '法学' },
  { value: 'lib', label: '图书馆' },
  { value: 'main', label: '综合' },
  { value: 'math', label: '数学' },
  { value: 'medical', label: '医学' },
  { value: 'mse', label: '材料' },
  { value: 'news', label: '热点' },
  { value: 'pharmacy', label: '药学' },
  { value: 'phil', label: '哲学' },
  { value: 'sfs', label: '外国语' },
  { value: 'shxy', label: '社会学' },
  { value: 'sky', label: '生科院' },
  { value: 'stat', label: '统计学' },
  { value: 'tas', label: '旅游学' },
  { value: 'wxy', label: '文学' },
  { value: 'yzb', label: '研招办' },
  { value: 'zfxy', label: '周政' }
]

const selectedSourceTypes = ref([])

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
    router.push({
      name: 'Search',
      query: {
        q: query.value,
        type: searchType.value,
        prefs: selectedSourceTypes.value.join(',')
      }
    })
  }
}
</script>

<style scoped>
.search-logs {
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

.history-and-preferences {
  display: flex;
  gap: 40px;
  margin-top: 20px;
}

.preferences {
  max-width: 400px;
  font-size: 14px;
  color: #444;
}

.preferences h4 {
  margin-bottom: 8px;
}

.checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 15px;
  max-height: 300px;
  overflow-y: auto;
  padding-right: 5px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: #fafafa;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 4px;
  user-select: none;
}
</style>
