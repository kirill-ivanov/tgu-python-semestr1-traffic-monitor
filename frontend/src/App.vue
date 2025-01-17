<script setup>
import {RouterLink, RouterView} from 'vue-router'
</script>

<template>
  <div class="app">
    <header>
      <RouterLink to="/">Онлайн</RouterLink>
      |
      <RouterLink to="/alerts">Уведомления</RouterLink>
      |
      <RouterLink to="/stats">Статистика</RouterLink>
    </header>
    <main>
      <RouterView/>
    </main>
  </div>

</template>

<style>
body {
  margin: 0;
  display: grid;
  place-items: flex-start;

}

.app {
  display: flex;
  flex-direction: column;
}

main {
  display: block;
}

header {
  display: inline;
  color: #111;
  margin: 0;
  padding: 0;
}
</style>
