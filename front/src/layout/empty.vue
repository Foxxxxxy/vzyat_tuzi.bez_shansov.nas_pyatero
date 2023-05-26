<script setup></script>

<template>
  <div class="layout layout--empty">
      <slot />
  </div>
</template>

<style scoped lang="scss">
.content {
  min-height: 100vh;
  padding: 50px 0 150px 0;
}
.layout--empty {
  max-height: 100vh;
  overflow: auto;
}
</style>
