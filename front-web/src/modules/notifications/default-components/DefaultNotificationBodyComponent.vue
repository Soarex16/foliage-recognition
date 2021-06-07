<template functional>
  <span class="whitespace-pre-wrap">{{notification.text}}</span>
</template>

<script>
export default {
  name: "DefaultNotificationBodyComponent",
  props: {
    notification: Object
  }
}
</script>
