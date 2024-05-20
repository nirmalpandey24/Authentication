<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-900" style="background-image: url('src/assets/image1.avif'); background-size: cover">
    <div class="max-w-md w-full bg-white shadow-md rounded-lg px-8 pt-6 pb-8 mb-4 opacity-70">
      <h1 class="text-3xl font-bold mb-4">Create New Blog Post</h1>
      <form @submit.prevent="createBlog">
        <div class="mb-6">
          <label for="title" class="block text-gray-700 text-sm font-bold mb-2">Title:</label>
          <input type="text" v-model="title" required class="shadow appearance-none border rounded w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
        </div>
        <div class="mb-6">
          <label for="description" class="block text-gray-700 text-sm font-bold mb-2">Description:</label>
          <textarea v-model="description" required class="shadow appearance-none border rounded w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"></textarea>
        </div>
        <div class="flex items-center justify-between mb-4">
          <button type="submit" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded focus:outline-none focus:shadow-outline">
            Create
          </button>
          <router-link to="/BlogPost" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded focus:outline-none focus:shadow-outline">
            own
          </router-link>
          <router-link to="/All" class="bg-indigo-500 hover:bg-indigo-700 text-white font-bold py-3 px-6 rounded focus:outline-none focus:shadow-outline">
            View All Posts
          </router-link>
          
          <button @click="logout" class="absolute top-0 right-0 mt-4 mr-4 bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
           Logout
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      title: '',
      description: ''
    };
  },
  methods: {
    async createBlog() {
      try {
        const token = localStorage.getItem('token'); 
        console.log('Token from localStorage:', token); 

        if (!token) {
          throw new Error('No token found');
        }

        await axios.post('http://127.0.0.1:8000/api/blog/', {
          title: this.title,
          description: this.description
        }, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        this.$router.push('BlogPost');
      } catch (error) {
        console.error('Error creating blog:', error);
      }
    },
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/');
      
    }
  }
};
</script>

<style scoped>
form {
  border-radius: 20px;
}
</style>
