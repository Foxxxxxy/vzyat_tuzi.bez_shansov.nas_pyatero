<script>
import { Line } from 'vue-chartjs'

export default {
  extends: Line,
  props: ['options'],
  mounted() {
    // this.chartData is created in the mixin.
    // If you want to pass options please create a local options object
    this.renderChart(this.chartData, this.options)
  },
  watch: {
    chartData() {
      this.$data._chart.update()
    },
    options() {
      this.$data._chart.destroy()
      this.renderChart(this.chartData, this.options)
    },
  },
}
</script>

<style scoped lang="scss"></style>
