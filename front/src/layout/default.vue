<script setup>
import { AppSidebar, AppHeader, AppFooter } from '~/components/app';
</script>

<template>
  <div class="layout">
    <app-header class="header" />
    <app-sidebar class="sidebar" />
    <div class="content">
      <slot />
    </div>
    <app-footer class="footer" />
  </div>
</template>

<style scoped lang="scss">
.layout {
  min-height: 100vh;
  display: grid;
  grid-template-columns: auto 4fr;
  grid-template-areas:
    'sidebar header'
    'sidebar content';
  @include md {
    height: 100vh;
    grid-template-columns: auto;
    grid-template-areas:
    'header'
    'content';
    grid-template-rows: 50px auto;
  }
}

.header {
  grid-area: header;
}

.sidebar {
  grid-area: sidebar;
  @include md {
    display: none;
  }
}

.footer {
  position: fixed;
  bottom: 0;
  display: none;
  overflow-x: auto;
  @include md {
    display: block;
  }
}

.content {
  grid-area: content;
  min-height: 100vh;
  height: 0;
  overflow: auto;
  background-color: #f6f6f8;
  padding: 50px;
  padding-bottom: 150px;
  @include md {
    padding: 50px 0;
    height: 100%;
    min-height: unset;
    padding-bottom: 150px;
  }
}
</style>
