<template>
    <form @submit.prevent="submitForm">
        <div>
            <label for="title">Title</label>
            <input type="text" v-model="title" placeholder="title">
        </div>
        <div>
            <label for="description">Description</label>
            <input type="text" v-model="description" placeholder="description">
        </div>
        <div>
            
        </div>
        <button type="submit" class="btn btn-success">Add User</button>
    </form>
</template>

<script>
import axios from 'axios';
export default {
    data() {
        return {
            form:{
            title: '',
            description: ''
            },
        };
    },
    methods: {
        submitForm() {
            axios.post('http://127.0.0.1:8000/users/customuser/', this.form)
        .then(response => {
          this.form = {
            title:'',
            description:''
          
          };
          this.toastMessage = 'User added successfully'; 
        });
        }
    }
}
</script>
