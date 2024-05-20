<template>
    <div class="max-w-4xl mx-auto py-8">
      <h1 class="text-3xl font-bold mb-4">All Blog Posts</h1>
      <div v-if="loading" class="text-gray-600">Loading...</div>
      <div v-else>
        <div v-if="error" class="text-red-600">{{ error }}</div>
        <div v-else>
          <div v-for="post in posts" :key="post.id" class="bg-white shadow-md mb-6 rounded-lg overflow-hidden">
            <div class="px-6 py-4">
              <div class="flex items-center justify-between mb-4">
                <div class="flex items-center">
                  
                  <div>
                    <p class="text-sm text-gray-700">Posted by {{ post.author }}</p>
                    <p class="text-xs text-gray-500">{{ formatDate(post.published_date) }}</p>
                  </div>
                </div>
                <button class="text-xs text-gray-600 hover:text-gray-800">Read more</button>
              </div>
              <h2 class="text-xl font-semibold mb-2">{{ post.title }}</h2>
              <p class="text-gray-700">{{ post.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        posts: [],
        loading: true,
        error: null
      };
    },
    created() {
      this.fetchPosts();
    },
    methods: {
      async fetchPosts() {
        try {
          const response = await axios.get('http://localhost:8000/api/blog/all/');
          this.posts = response.data;
          this.loading = false;
        } catch (error) {
          this.error = 'Error fetching posts. Please try again later.';
          console.error('Error fetching posts:', error);
          this.loading = false;
        }
      },
      formatDate(date) {
        return new Date(date).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
      }
    }
  };
  </script>
  
  <style scoped>
  
  .button {
    padding: 0.5rem 1rem;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  .button:hover {
    background-color: #45a049;
  }
  </style>
  