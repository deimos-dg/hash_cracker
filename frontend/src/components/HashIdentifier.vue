<template>
  <div class="hash-identifier">
    <el-card>
      <template #header>
        <div class="card-header">
          <h3>🔍 Identificar Tipo de Hash</h3>
        </div>
      </template>

      <el-input
        v-model="hashInput"
        placeholder="Ingresa el hash aquí..."
        clearable
        size="large"
        @keyup.enter="identifyHash"
        style="margin-bottom: 20px;"
      >
        <template #append>
          <el-button :loading="loading" @click="identifyHash">
            Identificar
          </el-button>
        </template>
      </el-input>

      <el-result
        v-if="result"
        :icon="resultIcon"
        :title="resultTitle"
        :sub-title="resultSubtitle"
      >
        <template #extra>
          <el-tag :type="resultTagType" size="large">
            {{ result.type }}
          </el-tag>
          <p>Longitud: {{ result.length }} caracteres</p>
          <p>Confianza: {{ result.confidence }}</p>
        </template>
      </el-result>

      <div v-if="error" class="error-message">
        <el-alert :title="error" type="error" show-icon />
      </div>

      <div v-if="!result && !loading" class="info-section">
        <el-alert title="Ejemplos de hashes para probar:" type="info" show-icon>
          <p><strong>MD5:</strong> 5f4dcc3b5aa765d61d8327deb882cf99 (password)</p>
          <p><strong>SHA-1:</strong> 7c4a8d09ca3762af61e59520943dc26494f8941b (123456)</p>
          <p><strong>SHA-256:</strong> 8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92 (123456)</p>
        </el-alert>
      </div>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios'

const API_BASE = 'http://localhost:5000/api'

export default {
  name: 'HashIdentifier',
  data() {
    return {
      hashInput: '',
      result: null,
      loading: false,
      error: ''
    }
  },
  computed: {
    resultIcon() {
      return this.result ? 'success' : 'info'
    },
    resultTitle() {
      return this.result ? 'Hash Identificado' : 'Ingresa un hash'
    },
    resultSubtitle() {
      return this.result ? 'Tipo de hash detectado' : 'Para comenzar la identificación'
    },
    resultTagType() {
      if (!this.result) return 'info'
      return this.result.confidence === 'high' ? 'success' :
             this.result.confidence === 'medium' ? 'warning' : 'danger'
    }
  },
  methods: {
    async identifyHash() {
      if (!this.hashInput.trim()) {
        this.error = 'Por favor ingresa un hash'
        return
      }

      this.loading = true
      this.error = ''
      this.result = null

      try {
        const response = await axios.post(`${API_BASE}/identify-hash`, {
          hash: this.hashInput
        })

        this.result = response.data
      } catch (error) {
        console.error('Error:', error)
        this.error = error.response?.data?.error || 'Error al conectar con el servidor'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.hash-identifier {
  max-width: 800px;
  margin: 0 auto;
}

.card-header {
  text-align: center;
}

.error-message {
  margin-top: 20px;
}

.info-section {
  margin-top: 20px;
}

.info-section p {
  margin: 5px 0;
  font-size: 12px;
}
</style>