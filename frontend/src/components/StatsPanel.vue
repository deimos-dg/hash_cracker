<template>
  <div class="stats-panel">
    <el-card>
      <template #header>
        <div class="card-header">
          <h3>📊 Estadísticas del Sistema</h3>
        </div>
      </template>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-statistic title="Contraseñas en diccionario" :value="stats.common_passwords_count || 0" />
        </el-col>
        <el-col :span="12">
          <el-statistic title="Estado del servicio" :value="stats.status || 'Desconocido'" />
        </el-col>
      </el-row>

      <el-divider />

      <h4>Información del Sistema</h4>
      <el-descriptions :column="1" border>
        <el-descriptions-item label="Versión">1.0.0</el-descriptions-item>
        <el-descriptions-item label="Backend URL">http://localhost:5000</el-descriptions-item>
        <el-descriptions-item label="Frontend URL">http://localhost:8080</el-descriptions-item>
        <el-descriptions-item label="Estado API">
          <el-tag :type="apiStatus === 'healthy' ? 'success' : 'danger'">
            {{ apiStatus }}
          </el-tag>
        </el-descriptions-item>
      </el-descriptions>

      <el-divider />

      <h4>Características</h4>
      <el-checkbox-group v-model="features" disabled>
        <el-checkbox label="Identificación automática de hashes" />
        <el-checkbox label="Cracking con diccionario común" />
        <el-checkbox label="Interfaz web moderna" />
        <el-checkbox label="API RESTful" />
        <el-checkbox label="Procesamiento multi-hilo" />
      </el-checkbox-group>

      <el-divider />

      <el-alert title="Nota:" type="warning" show-icon>
        Esta herramienta es para fines educativos. El cracking de hashes reales requiere
        hardware especializado y wordlists más grandes.
      </el-alert>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios'

const API_BASE = 'http://localhost:5000/api'

export default {
  name: 'StatsPanel',
  data() {
    return {
      stats: {},
      apiStatus: 'checking',
      features: [
        'Identificación automática de hashes',
        'Cracking con diccionario común',
        'Interfaz web moderna',
        'API RESTful',
        'Procesamiento multi-hilo'
      ]
    }
  },
  mounted() {
    this.loadStats()
    this.checkAPIHealth()
  },
  methods: {
    async loadStats() {
      try {
        const response = await axios.get(`${API_BASE}/stats`)
        this.stats = response.data
      } catch (error) {
        console.error('Error loading stats:', error)
      }
    },

    async checkAPIHealth() {
      try {
        const response = await axios.get(`${API_BASE}/health`)
        this.apiStatus = response.data.status
      } catch (error) {
        this.apiStatus = 'offline'
        console.error('API health check failed:', error)
      }
    }
  }
}
</script>

<style scoped>
.stats-panel {
  max-width: 800px;
  margin: 0 auto;
}

.card-header {
  text-align: center;
}

.el-checkbox {
  display: block;
  margin: 5px 0;
}
</style>