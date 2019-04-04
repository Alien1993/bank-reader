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
            :monday-first="true"
            :input-class="inputClass"
            v-model="fromDate"
          />
        </div>
      </div>
    </div>
    <div class="panel-block">
      <div class="field">
        <label class="label">Date to</label>
        <div class="control">
          <datepicker
            :monday-first="true"
            :input-class="inputClass"
            v-model="toDate"
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
import axios from 'axios';

@Component({
  components: {
    datepicker: Datepicker,
  },
})
export default class Form extends Vue {
@Prop({ default: 'input' }) public readonly inputClass!: string;
@Prop(String) private title!: string;
@Prop({ default: () => moment().subtract(2, 'weeks').toDate() }) private fromDate!: Date;
@Prop({ default: () => moment().toDate() }) private toDate!: Date;

  private getMovements() {
    const DATE_FORMAT = 'YYYY-MM-DD';
    const params = {
      date_from: moment(this.fromDate).format(DATE_FORMAT),
      date_to: moment(this.toDate).format(DATE_FORMAT),
    };
    const vm = this;
    axios.get('./api/movements', {params})
    .then((response) => {
      vm.$emit('success', response.data);
    })
    .catch((error) => {
      vm.$emit('error', error);
    });
  }
}
</script>


<style lang="scss" scoped>
.panel {
  position: fixed;
}
</style>
