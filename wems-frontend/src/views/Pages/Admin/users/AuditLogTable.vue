<template>
  <table>
    <thead>
      <tr>
        <th>User</th>
        <th>Action</th>
        <th>Target</th>
        <th>IP Address</th>
        <th>Device</th>
        <th>Time</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="log in logs" :key="log.id">
        <td>{{ log.user }}</td>
        <td>{{ log.action }}</td>
        <td>{{ log.targetType }}:{{ log.targetId }}</td>
        <td>{{ log.ip }}</td>
        <td>{{ log.device }}</td>
        <td>{{ log.time }}</td>
      </tr>
    </tbody>
  </table>
</template>
<script setup>
defineProps(['logs'])
</script>
