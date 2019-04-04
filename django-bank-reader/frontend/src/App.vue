<template>
  <div id="app">
    <Form
      v-on:success="setMovements($event)"
      v-on:error="appendNotification($event)"
    />
    <NotificationContainer
      id="notification-container"
      :notifications="notifications"
    />
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import Form from './components/Form.vue';
import NotificationContainer from './components/NotificationContainer.vue';

@Component({
  components: {
    Form,
    NotificationContainer,
  },
})
export default class App extends Vue {
@Prop({ default: () => [] }) private movements!: object[];
@Prop({ default: () => [] }) private notifications!: string[];

  private setMovements(movements: object[]) {
    this.movements = movements;
  }

  private appendNotification(text: string) {
    // Let's avoid notifications overload
    if (this.notifications.length >= 5) {
      this.notifications.splice(0, 1);
    }
    this.notifications.push(text);
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

#notification-container {
  position: fixed;
  bottom: 1rem;
  left: 1rem;
  width: 20%;
}
</style>
