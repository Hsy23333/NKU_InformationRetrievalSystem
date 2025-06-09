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

    <div class="guess-you-like" style="margin-top: 30px;">
      <h4>猜你喜欢喵</h4>
      <ul v-if="guessKeywords.length">
        <li
          v-for="(kw, index) in guessKeywords"
          :key="index"
          @click="goToGuessSearch(kw)"
          class="guess-item"
        >
          {{ kw }}
        </li>
      </ul>
      <div v-else>没有喵~</div>
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
const guessKeywords = ref([])
const selectedSourceTypes = ref([])

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

onMounted(() => {
  const logs = localStorage.getItem(STORAGE_KEY)
  if (logs) {
    searchLogs.value = JSON.parse(logs)
    generateGuessKeywords()
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
  generateGuessKeywords()
}

function clearLogs() {
  searchLogs.value = []
  localStorage.removeItem(STORAGE_KEY)
  guessKeywords.value = []
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

function goToGuessSearch(keyword) {
  router.push({
    name: 'Search',
    query: {
      q: keyword,
      type: 'normal',
      prefs: selectedSourceTypes.value.join(',')
    }
  })
}

function generateGuessKeywords() {
  const hotBackup = ['校园通知', '奖学金申请', '课程安排', '考试时间', '研究生推免', '四六级报名']
  const suffixes = ['通知', '讲座', '安排', '官网', '报名', '政策', '指南']
  const typeMap = {
    cs: ['软院通知', '程序设计', 'C++课设'],
    law: ['法考报名', '案例分析'],
    history: ['中国近代史', '史学讲座'],
    math: ['高数期末', '数学建模'],
    finance: ['金融实习', '经济形势'],
    medical: ['临床课程', '医学讲座']
  }

  if (!searchLogs.value.length && selectedSourceTypes.value.length === 0) {
    guessKeywords.value = hotBackup.slice(0, 6)
    return
  }

  const keywordParts = searchLogs.value
    .slice(0, 3)
    .flatMap(log => log.keyword.split(/[\s，。、“”·《》]/).filter(w => w.length >= 2))

  const combined = []

  keywordParts.forEach(part => {
    const shuffled = [...suffixes].sort(() => Math.random() - 0.5)
    shuffled.slice(0, 2).forEach(suf => {
      combined.push(part + suf)
    })
  })

  selectedSourceTypes.value.forEach(type => {
    if (typeMap[type]) {
      combined.push(...typeMap[type].slice(0, 2))
    }
  })

  guessKeywords.value = [...new Set(combined)].slice(0, 6)
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

.guess-you-like {
  max-width: 400px;
  font-size: 14px;
  color: #444;
}

.guess-you-like ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.guess-item {
  padding: 4px 6px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
}

.guess-item:hover {
  background-color: #f5f5f5;
}
</style>
