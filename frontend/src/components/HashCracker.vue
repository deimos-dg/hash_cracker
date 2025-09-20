<template>
  <div class="hash-cracker">
    <el-card>
      <template #header>
        <div class="card-header">
          <h3>🔓 Crackear Hash</h3>
        </div>
      </template>

      <el-form :model="form" label-width="120px">
        <el-form-item label="Algoritmo">
          <el-select v-model="form.algorithm" placeholder="Selecciona algoritmo">
            <el-option label="MD5" value="MD5" />
            <el-option label="SHA-1" value="SHA-1" />
            <el-option label="SHA-256" value="SHA-256" />
            <el-option label="SHA-512" value="SHA-512" />
          </el-select>
        </el-form-item>

        <el-form-item label="Hash a crackear">
          <el-input
            v-model="form.targetHash"
            placeholder="Ingresa el hash..."
            clearable
          />
        </el-form-item>

        <el-form-item label="Método">
          <el-radio-group v-model="form.method">
            <el-radio label="common">Diccionario común</el-radio>
            <el-radio label="rockyou" disabled>RockYou.txt</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            :loading="cracking"
            @click="startCracking"
            :disabled="!form.algorithm || !form.targetHash"
          >
            {{ cracking ? 'Crackeando...' : 'Iniciar Cracking' }}
          </el-button>

          <el-button
            v-if="cracking"
            type="danger"
            @click="stopCracking"
          >
            Detener
          </el-button>
        </el-form-item>
      </el-form>

      <el-progress
        v-if="cracking"
        :percentage="progressPercentage"
        :status="progressStatus"
        :text-inside="true"
      />

      <el-result
        v-if="result"
        :icon="result.success ? 'success' : 'error'"
        :title="result.success ? '¡Contraseña Encontrada!' : 'No se encontró'"
      >
        <template #extra>
          <div v-if="result.success">
            <el-tag type="success" size="large">
              🔓 {{ result.password }}
            </el-tag>
          </div>
          <div v-else>
            <p>La contraseña no se encontró en el diccionario</p>
          </div>

          <div v-if="result.stats" class="stats">
            <p>Palabras probadas: {{ result.stats.total_tested.toLocaleString() }}</p>
            <p>Velocidad: {{ Math.round(result.stats.words_per_second) }} palabras/segundo</p>
          </div>
        </template>
      </el-result>

      <div v-if="!cracking && !result" class="info-section">
        <el-alert title="Hashes de ejemplo para probar:" type="info" show-icon>
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
  name: 'HashCracker',
  data() {
    return {
      form: {
        algorithm: '',
        targetHash: '',
        method: 'common'
      },
      cracking: false,
      result: null,
      progressPercentage: 0
    }
  },
  computed: {
    progressStatus() {
      return this.cracking ? 'success' : 'exception'
    }
  },
  methods: {
    async startCracking() {
      this.cracking = true
      this.result = null

      try {
        const response = await axios.post(`${API_BASE}/crack-hash`, this.form)
        this.result = response.data
      } catch (error) {
        this.$message.error(error.response?.data?.error || 'Error al crackear el hash')
      } finally {
        this.cracking = false
        this.progressPercentage = 0
      }
    },

    async stopCracking() {
      try {
        await axios.post(`${API_BASE}/stop-crack`)
        this.cracking = false
        this.$message.info('Operación detenida')
      } catch (error) {
        this.$message.error('Error al detener la operación')
      }
    }
  }
}
</script>

<style scoped>
.hash-cracker {
  max-width: 800px;
  margin: 0 auto;
}

.stats {
  margin-top: 20px;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 4px;
}

.info-section {
  margin-top: 20px;
}

.info-section p {
  margin: 5px 0;
  font-size: 12px;
}
</style>