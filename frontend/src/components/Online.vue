<script>
export default {
  data: () => ({
    imgLink: 'result/out_result.jpg'
  }),
  mounted() {
    var self = this;
    setInterval(function () {
      self.updateImage()
    }, 1000)
  },
  methods: {
    updateImage() {
      let str = '../result/out_result.jpg?' + new Date().getTime();
      this.imgLink = str;
    }
  }
}
</script>

<template>
  <div>
    <h1>Онлайн</h1>
    <img :src="imgLink"/>
  </div>
</template>

<style scoped>
</style>