<template>
  <transition name="fade">
    <div v-if="show" class="toast">
      {{ message }}
    </div>
  </transition>
</template>

<script>
export default {
  props: {
    message: {
      type: String,
      required: true
    },
    duration: {
      type: Number,
      default: 3000 
    }
  },
  data() {
    return {
      show: false
    };
  },
  mounted() {
    this.show = true;
    setTimeout(() => {
      this.show = false;
    }, this.duration);
  }
};
</script>

<style scoped>
.toast {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(255, 69, 0, 0.9); 
  color: #fff;
  padding: 12px 24px; 
  border-radius: 8px; 
  z-index: 999;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); 
}

/* Animation */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>
