<template>
  <div id="app">
    <el-container style="min-height: 100vh;">
      <el-header style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-align: center; padding: 20px;">
        <h1>🔓 Hash Cracker Pro</h1>
        <p>Herramienta avanzada para identificación y cracking de hashes</p>
      </el-header>

      <el-main style="padding: 20px;">
        <el-tabs type="border-card" style="max-width: 1200px; margin: 0 auto;">
          <el-tab-pane label="🔍 Identificar Hash">
            <HashIdentifier />
          </el-tab-pane>

          <el-tab-pane label="🔓 Crackear Hash">
            <HashCracker />
          </el-tab-pane>

          <el-tab-pane label="📊 Estadísticas">
            <StatsPanel />
          </el-tab-pane>
        </el-tabs>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import HashIdentifier from './components/HashIdentifier.vue'
import HashCracker from './components/HashCracker.vue'
import StatsPanel from './components/StatsPanel.vue'

export default {
  name: 'App',
  components: {
    HashIdentifier,
    HashCracker,
    StatsPanel
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  margin: 0;
  padding: 0;
}

body {
  margin: 0;
  padding: 0;
  background-color: #f5f7fa;
}
</style>