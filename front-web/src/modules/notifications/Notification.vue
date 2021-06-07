<template>
  <div class="shadow-xl rounded-md px-4 py-2 flex" :class="styles.bg">
    <div class="w-6 h-6 mr-4">
      <component :is="styles.icon" class="w-auto h-full" :class="styles.iconColor"/>
    </div>

    <div class="flex flex-col">
      <span class="font-medium" :class="styles.header">
        <slot name="header"></slot>
      </span>

      <span class="font-normal" :class="styles.body">
        <slot name="body"></slot>
      </span>
    </div>

    <div v-show="dismissible" class="ml-auto mr-0">
      <button
          @click="closeNotification"
          class="ml-4 transition-colors duration-300 rounded-sm focus:outline-none focus:ring-2"
          :class="[styles.closeIconColor, styles.focusRing]"
      >
        <cross-icon class="w-6 h-6" :class="styles.iconColor"/>
      </button>
    </div>
  </div>
</template>

<script>
import WarningIcon from "@/components/icons/WarningIcon.vue";
import InfoIcon from "@/components/icons/InfoIcon.vue";
import ErrorIcon from "@/components/icons/ErrorIcon.vue";
import CheckIcon from "@/components/icons/CheckIcon.vue";
import CrossIcon from "@/components/icons/CrossIcon.vue";

const variants = ['info', 'warning', 'danger', 'success'];

const variantMapping = {
  'info': {
    icon: InfoIcon,
    iconColor: 'text-blue-400',
    bg: 'bg-blue-50',
    closeIconColor: 'hover:bg-blue-100',
    focusRing: 'focus:ring-blue-400',
    header: 'text-blue-600',
    body: 'text-blue-600'
  },
  'warning': {
    icon: WarningIcon,
    iconColor: 'text-yellow-500',
    bg: 'bg-yellow-50',
    closeIconColor: 'hover:bg-yellow-100',
    focusRing: 'focus:ring-yellow-400',
    header: 'text-yellow-900',
    body: 'text-yellow-800'
  },
  'danger': {
    icon: ErrorIcon,
    iconColor: 'text-red-400',
    bg: 'bg-red-50',
    closeIconColor: 'hover:bg-red-100',
    focusRing: 'focus:ring-red-400',
    header: 'text-red-800',
    body: 'text-red-800'
  },
  'success': {
    icon: CheckIcon,
    iconColor: 'text-green-500',
    bg: 'bg-green-50',
    closeIconColor: 'hover:bg-green-100',
    focusRing: 'focus:ring-green-400',
    header: 'text-green-900',
    body: 'text-green-800'
  }
}

export default {
  name: "Notification",
  components: {CrossIcon, WarningIcon},
  props: {
    variant: {
      type: String,
      default: 'info',
      validator(value) {
        return variants.indexOf(value) !== -1;
      }
    },
    dismissible: Boolean
  },
  computed: {
    styles() {
      return variantMapping[this.variant];
    }
  },
  methods: {
    closeNotification() {
      this.$emit('close');
    }
  }
}
</script>

