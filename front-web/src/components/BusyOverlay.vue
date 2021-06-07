<template v-once>
  <div class="flex flex-col justify-center items-center w-full h-full fixed block top-0 left-0 bg-black opacity-70 z-50">
    <spinner class="h-7 w-7"></spinner>
    <span class="text-white">Processing data</span>
  </div>
</template>

<script>
import Spinner from "./Spinner.vue";

export default {
  name: 'BusyOverlay',
  components: {Spinner}
}
</script>
