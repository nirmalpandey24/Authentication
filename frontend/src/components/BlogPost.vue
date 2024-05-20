<template>
  <div class="max-w-4xl mx-auto py-8 background-img">
    <h1 class="text-3xl font-bold mb-4 text-center">My Blog Posts</h1>
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
              <div class="flex space-x-2">
                <button @click="editPost(post)" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded focus:outline-none focus:shadow-outline">Edit</button>
                <button @click="deletePost(post.id)" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded focus:outline-none focus:shadow-outline">Delete</button>
              </div>
            </div>
            <h2 class="text-xl font-semibold mb-2">{{ post.title }}</h2>
            <p class="text-gray-700">{{ post.description }}</p>
          </div>
        </div>
      </div>
    </div>

    
    <div v-if="editingPost" class="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-75">
      <div class="bg-white shadow-md rounded-lg p-6 w-full max-w-md mx-auto">
        <h2 class="text-xl font-semibold mb-4">Edit Post</h2>
        <form @submit.prevent="updatePost">
          <div class="mb-4">
            <label for="title" class="block text-gray-700">Title:</label>
            <input v-model="editingPost.title" id="title" class="w-full border border-gray-300 rounded px-3 py-2" />
          </div>
          <div class="mb-4">
            <label for="description" class="block text-gray-700">Description:</label>
            <textarea v-model="editingPost.description" id="description" class="w-full border border-gray-300 rounded px-3 py-2"></textarea>
          </div>
          <button type="submit" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Update</button>
          <button @click="cancelEdit" class="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded ml-2">Cancel</button>
        </form>
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
      error: null,
      editingPost: null,
    };
  },
  created() {
    this.fetchPosts();
  },
  methods: {
    async fetchPosts() {
      try {
        const token = localStorage.getItem('token');
        console.log('Token from localStorage:', token);

        if (!token) {
          throw new Error('No token found');
        }

        const response = await axios.get('http://localhost:8000/api/blog/user/', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        this.posts = response.data;
        this.loading = false;
      } catch (error) {
        this.error = 'Error fetching posts. Please try again later.';
        console.error('Error fetching posts:', error);
        this.loading = false;
      }
    },
    async deletePost(postId) {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          throw new Error('No token found');
        }

        await axios.delete(`http://localhost:8000/api/blog/${postId}/`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        this.posts = this.posts.filter(post => post.id !== postId);
      } catch (error) {
        this.error = 'Error deleting post. Please try again later.';
        console.error('Error deleting post:', error);
      }
    },
    editPost(post) {
      this.editingPost = { ...post };
    },
    cancelEdit() {
      this.editingPost = null;
    },
    async updatePost() {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          throw new Error('No token found');
        }

        const response = await axios.put(`http://localhost:8000/api/blog/${this.editingPost.id}/`, {
          title: this.editingPost.title,
          description: this.editingPost.description
        }, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        const updatedPost = response.data;
        this.posts = this.posts.map(post => post.id === updatedPost.id ? updatedPost : post);
        this.editingPost = null;
      } catch (error) {
        this.error = 'Error updating post. Please try again later.';
        console.error('Error updating post:', error);
      }
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
    }
  }
};
</script>

<style scoped>

</style>
