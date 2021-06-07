<template>
  <card class="h-full w-full">
    <div class="flex justify-center items-center relative h-full w-full rounded-md border-2 border-gray-300 border-dashed">
      <div v-show="!value" class="absolute bg-white h-full w-full flex items-center justify-center">
        <span class="text-xl text-gray-400">Select images & press "Upload & recognize"</span>
      </div>
      <canvas class="w-full h-full" width="1900" height="1200" ref="canvas"></canvas>
    </div>
  </card>
</template>

<script>
import Card from "@/components/Card.vue";

const CLASS_COLOR_MAPPING = {
  1: '#ff00005f', // camouflage
  2: '#00ff005f' // foliage
};

export default {
  name: 'ResultView',
  components: {Card},
  props: {
    value: Object
  },
  watch: {
    value(newVal) {
      if (!newVal) return;

      const {result, img} = newVal;

      const reader = new FileReader();
      reader.onload = () => {
        const image = new Image();
        image.src = reader.result;
        image.onload = () => this.renderResult(result, image);
      };
      reader.readAsDataURL(img);
    }
  },
  methods: {
    renderResult(result, img) {
      const canvas = this.$refs['canvas'];

      const ctx = canvas.getContext('2d');

      const [TILE_WIDTH, TILE_HEIGHT] = result['tile_size'];
      const canvasWidth = canvas.width, canvasHeight = canvas.height;
      const imgWidth = img.width, imgHeight = img.height;

      const tileHorizontalCount = imgWidth / TILE_WIDTH, tileVerticalCount = imgHeight / TILE_HEIGHT;

      const canvasTileWidth = canvasWidth / tileHorizontalCount, canvasTileHeight = canvasHeight / tileVerticalCount;

      const tiles = result['tiles'];

      ctx.drawImage(img, 0, 0, canvasWidth, canvasHeight);
      tiles.forEach(tile => {
        ctx.fillStyle = CLASS_COLOR_MAPPING[tile.val];
        ctx.fillRect(tile.x * canvasTileWidth, tile.y * canvasTileHeight, canvasTileWidth, canvasTileHeight);
      });
    }
  }
}
</script>
