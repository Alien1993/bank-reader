<template>
  <nav class="panel">
    <p v-if="title" class="panel-heading">
      {{ title }}
    </p>
    <div class="panel-block">
      <div class="field">
        <label class="label">Date from</label>
        <div class="control">
          <datepicker
            :input-class="inputClass"
            :value="fromDate"
          />
        </div>
      </div>
    </div>
    <div class="panel-block">
      <div class="field">
        <label class="label">Date to</label>
        <div class="control">
          <datepicker
            :input-class="inputClass"
            :value="toDate"
          />
        </div>
      </div>
    </div>
    <div class="panel-block">
      <button
        class="button is-primary is-fullwidth"
        @click="getMovements"
      >
        Submit
      </button>
    </div>
  </nav>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import Datepicker from 'vuejs-datepicker';
import moment from 'moment';

@Component({
  components: {
    datepicker: Datepicker,
  },
})
export default class Form extends Vue {
@Prop({ default: 'input' }) public readonly inputClass!: string;
@Prop(String) private title!: string;
@Prop({ default: moment().subtract(2, 'weeks').valueOf() }) private fromDate!: moment.Moment;
@Prop({ default: moment().valueOf() }) private toDate!: moment.Moment;

  private getMovements() {
    // TODO: Here call API
  }
}
</script>


<style lang="scss" scoped>
.panel {
  position: fixed;
  width: 20%;
}
</style>
