<template>
  <div
    class="notification is-danger"
    @click.middle="close"
  >
    <button
      class="delete"
      @click="close"
    />
    {{ text }}
  </div>

</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class Notification extends Vue {
@Prop(Error) private text!: Error;

  private close() {
    this.$emit('close');
  }
}
</script>

