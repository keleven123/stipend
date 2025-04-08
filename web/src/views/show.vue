<template>
  <div class="container">
    <div class="screen">
      <h1>公示</h1>
      <div v-if="responseData" class="response-content">
        <h2>申请通过的学生如下</h2>
        <p>{{ responseData }}</p>
      </div>
      <div v-else-if="loading">数据加载中...</div>
      <div v-else>暂无数据</div>
    </div>
    <button @click="publishData" :disabled="loading" class="publish-button">公示</button>
  </div>
</template>

<script>
import { listApi } from '/src/api/suanfa';

export default {
  data() {
    return {
      responseData: null, // 存储 API 返回的数据
      loading: false, // 加载状态
    };
  },
  methods: {
    async publishData() {
      this.loading = true; // 开始加载
      try {
        // 调用 listApi 发送请求
        const response = await listApi({});
        console.log('Response Data:', response.data); // 打印 response.data
        this.responseData = response.data; // 将 API 返回的数据存储到 responseData
      } catch (error) {
        console.error('Error:', error); // 捕获并打印错误
      } finally {
        this.loading = false; // 结束加载
      }
    },
  },
};
</script>

<style>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #f0f0f0;
}

.screen {
  width: 80%;
  height: 60%;
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.publish-button {
  margin-top: 20px;
  padding: 10px 20px;
  font-size: 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.publish-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.publish-button:hover:not(:disabled) {
  background-color: #0056b3;
}

.response-content {
  margin-top: 20px;
}
</style>