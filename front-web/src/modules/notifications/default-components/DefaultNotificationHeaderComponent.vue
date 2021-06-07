<template functional>
  <span>{{notification.title}}</span>
</template>

<script>
export default {
  name: "DefaultNotificationBodyComponent",
  props: {
    notification: Object
  }
}
</script>
