<template>
  <div class="max-w-4xl mx-auto mt-10 p-6 bg-white rounded shadow">
    <h2 class="text-xl font-bold mb-4">User Table</h2>
    <table class="table-auto w-full border-collapse border border-gray-300">
      <thead>
        <tr class="bg-gray-100">
          <th class="border border-gray-300 px-4 py-2">Name</th>
          <th class="border border-gray-300 px-4 py-2">Email</th>
          <th class="border border-gray-300 px-4 py-2">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td class="border border-gray-300 px-4 py-2">{{ user.name }}</td>
          <td class="border border-gray-300 px-4 py-2">{{ user.email }}</td>
          <td class="border border-gray-300 px-4 py-2">
            <button @click="editUser(user)" class="bg-blue-500 text-white px-2 py-1 rounded">Edit</button>
            <button @click="deleteUser(user.id)" class="bg-red-500 text-white px-2 py-1 rounded ml-2">Delete</button>
            <button @click="viewUser(user)" class="bg-green-500 text-white px-2 py-1 rounded ml-2">View</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Edit User Modal -->
    <div v-if="showModal" class="fixed inset-0 flex items-center justify-center z-50">
      <div class="modal-overlay absolute inset-0 bg-black opacity-50"></div>
      <div class="modal-container bg-white w-11/12 md:w-1/3 mx-auto rounded shadow-lg z-50 overflow-y-auto">
        <div class="modal-content py-4 text-left px-6">
          <span @click="closeModal" class="absolute top-0 right-0 p-4 cursor-pointer">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </span>
          <h3 class="text-lg font-semibold mb-4">{{ modalData?.id ? 'Edit User' : 'View User' }}</h3>
          <div class="modal-body">
            <div v-if="modalData" class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700">Name</label>
                <input v-model="modalData.name" type="text" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-opacity-50" :readonly="!modalData.id" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Email</label>
                <input v-model="modalData.email" type="email" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-opacity-50" :readonly="!modalData.id" />
              </div>
            </div>
          </div>
          <div class="modal-footer flex justify-end mt-4">
            <button @click="closeModal" class="bg-gray-300 text-gray-700 px-4 py-2 rounded-md mr-2">Cancel</button>
            <button v-if="modalData?.id" @click="updateUser(modalData)" class="bg-blue-500 text-white px-4 py-2 rounded-md">Update</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface User {
  id: number;
  name: string;
  email: string;
}

const users = ref<User[]>([])
const showModal = ref(false);
const modalData = ref<User | null>(null);

const deleteUser = async (id: number) => {
  try {
    const res = await fetch(`http://localhost:8000/tahsin/${id}`, {
      method: 'DELETE'
    })
    if (res.ok) {
      users.value = users.value.filter(user => user.id !== id)
    } else {
      console.error('Failed to delete user')
    }
  } catch (error) {
    console.error('Error deleting user:', error)
  }
}

const openModal = (user: User) => {
  modalData.value = user;
  showModal.value = true;
};

const closeModal = () => {
  modalData.value = null;
  showModal.value = false;
};

const editUser = (user: User) => {
  openModal(user);
};

const viewUser = (user: User) => {
  openModal(user);
};

const updateUser = async (user: User) => {
  try {
    const res = await fetch(`http://localhost:8000/tahsin/${user.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(user)
    });
    if (res.ok) {
      const updatedUser = await res.json();
      const index = users.value.findIndex(u => u.id === updatedUser.id);
      if (index !== -1) {
        users.value[index] = updatedUser;
      }
      closeModal();
    } else {
      console.error('Failed to update user');
    }
  } catch (error) {
    console.error('Error updating user:', error);
  }
};

// Restored fetchUsers function
const fetchUsers = async () => {
  try {
    const res = await fetch('http://localhost:8000/tahsin');
    const data = await res.json();
    users.value = data;
  } catch (error) {
    console.error('Error fetching users:', error);
  }
};

// Call fetchUsers on component mount
onMounted(() => {
  fetchUsers();
});
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  z-index: 50;
}

.modal-container {
  position: relative;
  width: 90%;
  max-width: 500px;
  margin: 1.75rem auto;
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  z-index: 100;
}

.modal-content {
  padding: 1.5rem;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 500;
}

.modal-close {
  cursor: pointer;
  font-size: 1.25rem;
}

.modal-body {
  margin-top: 1rem;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 1.5rem;
}

.modal-footer button {
  margin-left: 0.5rem;
}
</style>
