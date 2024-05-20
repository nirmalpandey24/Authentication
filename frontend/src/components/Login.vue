<template>
  <div class="flex justify-center items-center h-screen" style="background-image: url('src/assets/image.avif'); background-size: cover;">
    <div class="w-full max-w-sm">
      <h2 class="text-2xl font-semibold mb-4 text-center">Login</h2>
      <form @submit.prevent="login" class="bg-gray-500 shadow-md rounded px-8 pt-6 pb-8 mb-4 border-10 border-gray-300">
        <div class="mb-4">
          <label for="email" class="block text-white text-sm font-bold mb-2">Email:</label>
          <input type="email" id="email" v-model="email" required class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
        </div>
        <div class="mb-6">
          <label for="password" class="block text-white text-sm font-bold mb-2">Password:</label>
          <input type="password" id="password" v-model="password" required class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline">
        </div>
        <button type="submit" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">Login</button>
        <router-link to="/user-form" class="block text-center mt-4">
          <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full">Click here to register</button>
        </router-link>
      </form>
      <CustomToast :message="toastMessage" :duration="toastDuration" v-if="toastVisible" />
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import CustomToast from '@/components/CustomToast.vue';
      

export default {
  components: {
    CustomToast
  },
  data() {
    return {
      email: '',
      password: '',
      toastMessage: '',
      toastDuration: 3000,
      toastVisible: false
    };
  },
  methods: {
    login() {
      axios
        .post('http://127.0.0.1:8000/users/login', {
          email: this.email,
          password: this.password
        })
        .then(response => {
          
          const token = response.data.token;
          localStorage.setItem('token', token);

          
          this.toastMessage = 'Login successful';
          this.toastDuration = 2000;
          this.showToast();


         
          
          setTimeout(() => {
            this.$router.push({ name: 'blog' });
          }, 1000);
        })
        .catch(error => {
          
          this.toastMessage = error.response?.data?.detail || 'Login failed';
          this.toastDuration = 5000;
          this.showToast();
        });
    },
    showToast() {
      this.toastVisible = true;
      setTimeout(() => {
        this.toastVisible = false;
      }, this.toastDuration);
    }
  }
};
</script>

<style scoped>

</style>
