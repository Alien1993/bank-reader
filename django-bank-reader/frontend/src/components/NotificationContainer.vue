<template>
  <div class="container">
    <div v-for="(text, index) in notifications" v-bind:key="index">
      <Notification
        :text="text"
        @close="handleClose(index)"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import Notification from './Notification.vue';

@Component({
  components: {
    Notification,
  },
})
export default class NotificationContainer extends Vue {
@Prop({ default: () => [] }) public notifications!: string[];

  private handleClose(index: number) {
    this.notifications.splice(index, 1);
  }
}
</script>

<style lang="scss" scoped>
.container {
  display: flex;
  flex-flow: column;
  justify-content: space-between;

  * {
    margin-top: 0.3rem;
  }
}
</style>
