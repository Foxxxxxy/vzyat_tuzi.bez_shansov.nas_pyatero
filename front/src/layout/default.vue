<script setup>
import { AppSidebar, AppHeader } from '~/components/app';
</script>

<template>
  <div class="layout">
    <app-header class="header" />
    <app-sidebar class="sidebar" />
    <div class="content">
      <slot />
    </div>
  </div>
</template>

<style scoped lang="scss">
.layout {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 1fr 4fr;
  grid-template-areas:
    'sidebar header'
    'sidebar content';
}

.header {
  grid-area: header;
}

.sidebar {
  grid-area: sidebar;
}

.content {
  grid-area: content;
  min-height: 100vh;
  background-color: #f6f6f8;
  padding: 50px;
}
</style>
