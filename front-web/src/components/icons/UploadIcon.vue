<template v-once>
  <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 24 24">
    <path class="bounce" id="arrow" stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M12 4 12 16M16 12l-4 4m0 0L8 12M12 16" />
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1"/>
  </svg>
</template>

<script>
export default {
  name: "UploadIcon"
}
</script>

<style scoped>
  .bounce {
    animation: bounce 1s infinite;
  }

  @keyframes bounce {
    0%, 100% {
      transform: translateY(-10%);
      animation-timing-function: cubic-bezier(0.8, 0, 1, 1);
    }
    50% {
      transform: translateY(5%);
      animation-timing-function: cubic-bezier(0, 0, 0.2, 1);
    }
  }
</style>
