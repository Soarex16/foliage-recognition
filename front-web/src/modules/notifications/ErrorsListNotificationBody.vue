<template>
  <ul>
    <li v-for="err in notification.text">
      <b>{{ err[0] }}:</b> {{ err[1] }}
    </li>
  </ul>
</template>

<script>
export default {
  name: "ErrorsListNotificationBody",
  props: {
    notification: Object
  }
}
</script>
