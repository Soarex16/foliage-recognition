<template>
  <div class="absolute left-0 bottom-0 overflow-y-hidden max-h-screen max-w-xl p-4 space-y-2 z-40">
    <transition-group
      leave-active-class="absolute hidden"
      enter-from-class="opacity-0"
      leave-to-class="opacity-0"
    >
      <notification
        class="transition-all inline-block duration-800 ease-in-out"
        v-for="(n, idx) in notifications"
        :key="idx"
        :variant="n.level"
        :dismissible="n.dismissible"
        @close="removeNotification(n.id)"
      >
        <template v-slot:header>
          <component :is="n.headerComp || DefaultNotificationHeaderComponent" :notification="n"/>
        </template>

        <template v-slot:body>
          <component :is="n.bodyComp || DefaultNotificationBodyComponent" :notification="n"/>
        </template>
      </notification>
    </transition-group>
  </div>
</template>

<script setup>
import {inject} from "vue";

import Notification from "./Notification.vue";
import {NOTIFICATIONS_INTERNAL_DATA_CONTEXT_KEY} from "./NotificationManager";

import DefaultNotificationBodyComponent from "./default-components/DefaultNotificationBodyComponent.vue";
import DefaultNotificationHeaderComponent from "./default-components/DefaultNotificationHeaderComponent.vue";

import nop from "@/utils/nop";

const defaultAlertContext = {
  notifications: [],
  removeNotification: nop,
  clearAll: nop
};

const {notifications, removeNotification, clearAll} = inject(NOTIFICATIONS_INTERNAL_DATA_CONTEXT_KEY, defaultAlertContext);
</script>
