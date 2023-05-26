<script setup>
defineProps({
  width: String,
  height: String,
  background: String,
  isActive: Boolean,
});
</script>

<template>
  <div
    :style="{ width: width + 'px', height: height + 'px' }"
    class="burger"
    :class="{active: isActive}"
  >
    <div :style="{ backgroundColor: background }" class="line"></div>
    <div :style="{ backgroundColor: background }" class="line"></div>
    <div :style="{ backgroundColor: background }" class="line"></div>
  </div>
</template>

<style lang="scss" scoped>

@keyframes round {
  from {
    transform: rotate(0deg)
  }
  to {
    transform: rotate(360deg)
  }
}
.burger {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
  &.active {
    animation: round 0.2s ease;
    justify-content: center;
    .line {
      transform-origin: center;
      &:first-child {
        transform: rotate(-45deg);
      }
      &:nth-child(2) {
        opacity: 0;
        position: absolute;
      }
      &:last-child {
        transform: rotate(45deg);
        position: absolute;
      }
    }
  }
}
.line {
  width: 100%;
  height: 3px;
  border-radius: 5px;
  flex: none;
  transition: transform 0.1s ease, opacity 0.1s ease;
}
</style>
