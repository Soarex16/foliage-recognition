<template>
  <div class="grid grid-rows-5 xl:grid-cols-5 gap-4 h-screen p-4 bg-gray-100">
    <div class="row-span-3 xl:row-span-5 xl:col-span-4">
      <slot name="left"></slot>
    </div>

    <div class="row-span-2 xl:row-span-5 xl:col-span-1 overflow-auto">
      <slot name="right"></slot>
    </div>
  </div>
</template>

<script>
import Card from "@/components/Card.vue";

export default {
  name: "SplitPanel",
  components: {
    Card
  }
}
</script>
