import {ref} from "vue";

import generateId from "@/utils/generateId";

export const NOTIFICATIONS_INTERNAL_DATA_CONTEXT_KEY = Symbol("notifications-queue");
const ALERT_TIMEOUT_TIMER = Symbol("timeout-timer");

/**
 * Notification system module for Vue
 * @type {{install(app): void}} - hook which called by Vue on module initialization
 */
export const NotificationManager = {
    install(app) {
        // storage for all notifications to show
        const notifications = ref([]);

        // callback for removing notification from internal storage
        const removeNotification = (id, timeout = false) => {
            const nIdx = notifications.value.findIndex(n => n?.id === id);
            if (nIdx === -1) {
                return -1;
            }

            const removedNotification = notifications.value.splice(nIdx, 1);

            if (!timeout) {
                clearTimeout(removedNotification[ALERT_TIMEOUT_TIMER]);
            }
        };

        /**
         * Function for creating new notification
         * @param notification {Object} - notification object
         */
        const alert = (notification) => {
            notification.id = generateId();
            // if notification doesn't have a timeout,
            // make alert dismissible to prevent persistent notifications
            if (notification.dismissible === false || !notification.timeout) {
                notification.dismissible = true;
            }

            if (notification.timeout) {
                notification[ALERT_TIMEOUT_TIMER] = setTimeout(
                    () => removeNotification(notification.id, true),
                    notification.timeout * 1000
                );
            }

            notifications.value.push(notification);
        };

        const clearAll = () => notifications.value = [];

        app.config.globalProperties.$alert = alert;
        app.provide(NOTIFICATIONS_INTERNAL_DATA_CONTEXT_KEY, {
            notifications,
            removeNotification,
            clearAll
        });
    }
}
