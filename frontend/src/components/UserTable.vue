<template>
  <div class="bg-gray-100 min-h-screen flex justify-center items-center ">
    <div class="max-w-full w-full bg-white rounded-lg shadow-md flex flex-col">
      <div class="flex justify-between items-center py-2 px-4">
        <h3 class="text-2xl font-bold mb-0 text-center">User Table</h3>
        <router-link to="/user-form" class="block">
          <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full">View User Form</button>
        </router-link>
      </div>
      <div class="overflow-x-auto" style="height: 1000px;"> 
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-200">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-800 uppercase tracking-wider">Email</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-800 uppercase tracking-wider">Name</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-800 uppercase tracking-wider">Salary</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-800 uppercase tracking-wider">Username</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-800 uppercase tracking-wider">Phone Number</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-800 uppercase tracking-wider">Address</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-800 uppercase tracking-wider">Gender</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-800 uppercase tracking-wider">Hobbies</th>
              <th class="px-6 py-3 text-xs font-medium text-gray-800 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="(user, index) in users" :key="index">
              <td class="px-6 py-4">{{ user.email }}</td>
              <td class="px-6 py-4">{{ user.ename }}</td>
              <td class="px-6 py-4">{{ user.esalary }}</td>
              <td class="px-6 py-4">{{ user.username }}</td>
              <td class="px-6 py-4">{{ user.phone_number }}</td>
              <td class="px-6 py-4">{{ user.address }}</td>
              <td class="px-6 py-4">{{ user.gender }}</td>
              <td class="px-6 py-4">{{ user.hobbies }}</td>
              <td class="px-6 py-4">
                <button @click="editUserClicked(user)" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full">Edit</button>
                <button @click="deleteUser(user.id)" class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-full">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50" v-if="editUserId !== null">
      <div class="bg-white rounded-lg shadow-md w-full max-w-3xl p-8">
        <span class="close absolute top-0 right-0 px-4 py-3 cursor-pointer text-gray-800" @click="cancelEdit">&times;</span>
        <h2 class="text-lg font-bold py-4">Edit User</h2>
        <form @submit.prevent="submitForm" class="space-y-4">
          <div>
            <label for="email" class="block text-gray-800">Email:</label>
            <input type="email" id="email" v-model="editUserForm.email" required class="input-field border border-gray-300 rounded-md p-2 w-full">
          </div>
          <div class="flex flex-wrap -mx-2">
            <div class="w-full md:w-1/2 px-2">
              <label for="phone" class="block text-gray-800">Phone:</label>
              <input type="tel" id="phone" v-model="editUserForm.phone_number" required class="input-field border border-gray-300 rounded-md p-2 w-full">
            </div>
            <div class="w-full md:w-1/2 px-2">
              <label for="name" class="block text-gray-800">Name:</label>
              <input type="text" id="name" v-model="editUserForm.ename" required class="input-field border border-gray-300 rounded-md p-2 w-full">
            </div>
          </div>
          <div>
            <label for="address" class="block text-gray-800">Address:</label>
            <input type="text" id="address" v-model="editUserForm.address" required class="input-field border border-gray-300 rounded-md p-2 w-full">
          </div>
          <div class="flex flex-wrap -mx-2">
            <div class="w-full md:w-1/2 px-2">
              <label for="salary" class="block text-gray-800">Salary:</label>
              <input type="number" id="salary" v-model="editUserForm.esalary" required class="input-field border border-gray-300 rounded-md p-2 w-full">
            </div>
            <div class="w-full md:w-1/2 px-2">
              <label for="gender" class="block text-gray-800">Gender:</label>
              <select id="gender" v-model="editUserForm.gender" required class="input-field border border-gray-300 rounded-md p-2 w-full">
                <option value="M">Male</option>
                <option value="F">Female</option>
                <option value="O">Other</option>
              </select>
            </div>
          </div>
          <div>
            <label for="username" class="block text-gray-800">Username:</label>
            <input type="text" id="username" v-model="editUserForm.username" required class="input-field border border-gray-300 rounded-md p-2 w-full">
          </div>
          <div>
            <label for="hobbies" class="block text-gray-800">Hobbies:</label>
            <input type="text" id="hobbies" v-model="editUserForm.hobbies" required class="input-field border border-gray-300 rounded-md p-2 w-full">
          </div>
          <button type="submit" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full">Update User</button>
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
      users: [],
      editUserId: null,
      editUserForm: {
        id: null,
        ename: '',
        email: '',
        esalary: '',
        username: '',
        phone_number: '',
        address: '',
        gender: '',
        hobbies: ''
      }
    };
  },
  mounted() {
    this.fetchUsers();
  },
  methods: {
    fetchUsers() {
      axios.get('http://127.0.0.1:8000/users/customuser/')
        .then(response => {
          this.users = response.data.filter(user => !user.isDeleted).map(user => ({ ...user, isEditing: false }));
        })
        .catch(error => {
          console.error('Error fetching users:', error);
        });
    },
    editUserClicked(user) {
      this.editUserId = user.id;
      this.editUserForm = { ...user };
    },
    saveChanges() {
      axios.put(`http://127.0.0.1:8000/users/customuser/${this.editUserForm.id}/`, this.editUserForm)
        .then(response => {
          this.editUserId = null;
          this.fetchUsers(); 
        })
        .catch(error => {
          console.error('Error updating user:', error);
        });
    },
    cancelEdit() {
      this.editUserId = null;
    },
    deleteUser(userId) {
      axios.delete(`http://127.0.0.1:8000/users/customuser/${userId}`)
        .then(response => {
          console.log('User deleted:', userId);
          this.fetchUsers(); 
        })
        .catch(error => {
          console.error('Error deleting user:', error);
        });
    },
    submitForm() {
      this.saveChanges();
    }
  }
};
</script>

<style>

</style>
