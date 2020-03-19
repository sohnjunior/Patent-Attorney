<template>
  <v-alert 
    v-model="show" 
    dense 
    outlined 
    :dismissible="true" 
    type="error"
    width="25rem" 
    transition="scale-transition"
    @input="clickCancel">
    {{ alertText }}
  </v-alert>
</template>

<script>
export default {
  props: { 'alertText': String, 'showAlert': Boolean },
  data() {
    return {
      show: this.showAlert,
    }
  },
  watch: {
    showAlert: function(newVal) {
      this.show = newVal;
    }
  },
  methods: {
    clickCancel() {
      this.$emit('cancel');
    }
  }
}
</script>

<style>
</style>