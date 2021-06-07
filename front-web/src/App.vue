<template>
  <notification-bar/>
  <split-panel>
    <template v-slot:left>
      <result-view :value="result"/>
    </template>

    <template v-slot:right>
      <input-form
          @request-start="loading = true"
          @request-finish="showResult"
      />
    </template>
  </split-panel>
  <busy-overlay v-show="loading"/>
</template>

<script>
import {shallowRef} from "vue";

import ResultView from "@/components/ResultView.vue";
import InputForm from "@/components/InputForm.vue";
import SplitPanel from "@/components/SplitPanel.vue";
import BusyOverlay from "@/components/BusyOverlay.vue";
import {NotificationBar, ErrorsListNotificationBody} from "@/modules/notifications/";
import {AppError} from "@/api";

export default {
  name: "App",
  components: {
    NotificationBar,
    BusyOverlay,
    SplitPanel,
    InputForm,
    ResultView
  },
  data() {
    return {
      loading: false,
      result: undefined,
      cnt: 0
    }
  },
  methods: {
    showResult(value, err) {
      this.loading = false;

      if (err) {
        let errTitle, errBody;

        if (err instanceof AppError) {
          errTitle = err.details.errorTitle;
          errBody = err.details.errorBody;
        } else if (typeof err === "string") {
          errBody = err;
        }

        const bodyComponentRef = shallowRef(ErrorsListNotificationBody);
        this.$alert({
          title: errTitle || `Error occurred while processing request`,
          text: errBody,
          level: 'danger',
          dismissible: true,
          bodyComp: Array.isArray(errBody) && bodyComponentRef
        });
        this.result = undefined;
        return;
      }

      this.result = shallowRef(value);
    }
  }
}
</script>
