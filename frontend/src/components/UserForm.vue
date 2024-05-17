<template>

  <div class="bg-green-200 min-h-screen flex justify-center items-center">
    <div class="max-w-xl w-full bg-gray-900 rounded-lg p-8">
      <form @submit.prevent="submitForm" class="space-y-4">
        <div>
          <label for="email" class="text-white block">Email:</label>
          <input type="email" id="email" v-model="form.email" required class="input-field">
        </div>
        <div class="flex flex-wrap -mx-2">
          <div class="w-full md:w-1/2 px-2">
            <label for="phone" class="text-white block">Phone:</label>
            <input type="tel" id="phone" v-model="form.phone_number" required class="input-field">
          </div>
          <div class="w-full md:w-1/2 px-2">
            <label for="name" class="text-white block">Name:</label>
            <input type="text" id="name" v-model="form.ename" required class="input-field">
          </div>
        </div>
        <div>
          <label for="address" class="text-white block">Address:</label>
          <input type="text" id="address" v-model="form.address" required class="input-field">
        </div>
        <div class="flex flex-wrap -mx-2">
          <div class="w-full md:w-1/2 px-2">
            <label for="salary" class="text-white block">Salary:</label>
            <input type="number" id="salary" v-model="form.esalary" required class="input-field">
          </div>
          <div class="w-full md:w-1/2 px-2">
            <label for="gender" class="text-white block">Gender:</label>
            <select id="gender" v-model="form.gender" required class="input-field">
              <option value="M">Male</option>
              <option value="F">Female</option>
              <option value="O">Other</option>
            </select>
          </div>
        </div>
        <div>
          <label for="username" class="text-white block">Username:</label>
          <input type="text" id="username" v-model="form.username" required class="input-field">
        </div>
        <div>
          <label for="hobbies" class="text-white block">Hobbies:</label>
          <input type="text" id="hobbies" v-model="form.hobbies" required class="input-field">
        </div>
        <div>
          <label for="password" class="text-white block">Password:</label>
          <input type="password" id="password" v-model="form.password" required class="input-field">

        </div>
        <button type="submit" class="btn btn-success">Add User</button>
      </form>
      <router-link to="/" class="block text-center mt-4">
        <button class="btn btn-primary">GO TO SIGIN</button>
      </router-link>
      <CustomToast :message="toastMessage" v-if="toastMessage" />
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
      form: {
        email: '',
        phone_number: '',
        ename: '',
        address: '',
        esalary: '',
        gender: '',
        username: '',
        hobbies: '',
        password:'',
      },
      toastMessage: '' 
    };
  },
  methods: {
    submitForm() {
      axios.post('http://127.0.0.1:8000/users/customuser/', this.form)
        .then(response => {
          this.form = {
            email: '',
            phone_number:'',
            ename: '',
            address: '',
            esalary: '',
            gender: '',
            username: '',
            hobbies: '',
            password:''
          };
          this.toastMessage = 'User added successfully'; 
        });
    },
  },
};
</script>

<style scoped>
  .input-field {
  width: 100%;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  border: 1px solid #ccc;
  background-color: #4a5568;
  color: #fff;
  outline: none;
}

.btn {
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  outline: none;
}

.btn-success {
  background-color: #48bb78;
  color: #fff;
}

.btn-primary {
  background-color: #4299e1;
  color: #fff;
}

.btn:hover {
  filter: brightness(1.2);
}

</style>
