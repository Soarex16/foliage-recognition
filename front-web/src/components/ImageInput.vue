<template>
  <div
      class="flex-1 min-w-fit"
  >
    <label class="block text-sm font-medium text-gray-700">
      {{title}}
    </label>

    <div class="border-2 border-gray-300 border-dashed rounded-md">
      <div
          v-if="!modelValue || !fileSrc"
          class="mt-1 flex justify-center px-6 pt-5 pb-6"
          @dragover.prevent="startDrag" @dragenter="startDrag"
          @dragleave="stopDrag" @drop.prevent="updateInput"
      >
        <div class="space-y-1 text-center">
          <div>
            <upload-icon v-if="isDragging"></upload-icon>
            <image-icon v-else/>
          </div>

          <div class="flex text-sm text-gray-600">
            <label :for="id" class="relative cursor-pointer bg-white rounded-md font-medium text-indigo-600 hover:text-indigo-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-indigo-500">
              <span>Choose a file</span>
              <input
                  :id="id"
                  :name="id"
                  type="file"
                  accept="image/*"
                  class="sr-only"
                  @change="updateInput"
              >
            </label>
            <p class="pl-1">or drag and drop</p>
          </div>

          <p class="text-xs text-gray-500">
            PNG, JPG up to 10MB
          </p>
        </div>
      </div>

      <div v-else class="relative">
        <div class="absolute left-0 top-0 h-full w-full rounded-md floor-fade"></div>
        <img class="object-contain rounded-md" :src="fileSrc" alt="file upload preview"/>

        <div class="absolute p-2 w-full bottom-0 flex justify-between items-end">
          <span class="break-all text-white">{{fileName}}</span>

          <button
              @click="clearInput"
              class="shadow-xl p-1 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-white">
            <delete-icon/>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ImageIcon from "./icons/ImageIcon.vue";
import UploadIcon from "./icons/UploadIcon.vue";
import DeleteIcon from "./icons/DeleteIcon.vue";

export default {
  name: 'ImageInput',
  components: {DeleteIcon, UploadIcon, ImageIcon},
  props: {
    title: String,
    id: String,
    modelValue: File
  },
  data() {
    return {
      isDragging: false,
      fileSrc: ''
    }
  },
  methods: {
    startDrag() {
      this.isDragging = true;
    },
    stopDrag(e) {
      if (e.target !== e.currentTarget)
        return;

      this.isDragging = false;
    },
    updateInput(e) {
      this.isDragging = false;

      const files = e.dataTransfer?.files || e.target.files;
      const file = files[0];

      this.$emit('update:modelValue', file);
    },
    clearInput() {
      this.$emit('update:modelValue', undefined);
      this.fileSrc = '';
    }
  },
  computed: {
    fileName() {
      return this.modelValue?.name;
    }
  },
  watch: {
    modelValue(val) {
      if (!val) {
        this.fileSrc = '';
        return;
      }

      const reader = new FileReader();
      reader.onload = (progressEvent) => this.fileSrc = progressEvent.target.result;
      return reader.readAsDataURL(val);
    }
  }
}
</script>

<style scoped>
  .min-w-fit {
    min-width: fit-content;
  }

  .floor-fade {
    background: linear-gradient(
        rgba(0, 0, 0, 0) 0%,
        rgba(0, 0, 0, 0) 50%,
        rgba(0, 0, 0, 0.6) 100%
    );
  }
</style>
