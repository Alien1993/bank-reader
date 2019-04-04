<template>
  <div id="app">
    <Form
      v-on:success="setMovements($event)"
    />
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import Form from './components/Form.vue';

@Component({
  components: {
    Form,
  },
})
export default class App extends Vue {
@Prop({ default: () => [] }) private movements!: object[];

  private setMovements(movements: object[]) {
    this.movements = movements;
  }
}
</script>

<style lang="scss">
@import "bulma";

#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  margin-top: 3rem;
  margin-left: 3rem;
  margin-right: 3rem;
}
</style>
