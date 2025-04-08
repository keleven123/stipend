<template>
  <div class="page-view">
    <div class="table-operations">
      <a-button type="primary" @click="getDataList">公示</a-button>
    </div>

    <!-- 通过名单 -->
    <h1>通过名单（{{ data.userList.length }}人）</h1>
    <a-table
        size="middle"
        :rowKey="record => record.student_id"
        :loading="data.loading"
        :columns="columns"
        :data-source="data.userList"
        :pagination="{
          size: 'default',
          current: data.page,
          pageSize: data.pageSize,
          onChange: (current) => (data.page = current),
          showSizeChanger: false,
          showTotal: (total) => `共${total}条数据`,
        }"
    >
      <template #emptyText>
        <a-empty description="目前暂无通过学生" />
      </template>
    </a-table>

    <!-- 未通过名单 -->
    <h1 style="margin-top: 40px">未通过名单（{{ data.unselectedList.length }}人）</h1>
    <a-table
        size="middle"
        :rowKey="record => record.student_id"
        :loading="data.loading"
        :columns="columns"
        :data-source="data.unselectedList"
        :pagination="{
          size: 'default',
          current: data.page,
          pageSize: data.pageSize,
          onChange: (current) => (data.page = current),
          showSizeChanger: false,
          showTotal: (total) => `共${total}条数据`,
        }"
    >
      <template #emptyText>
        <a-empty description="目前暂无未通过学生" />
      </template>
    </a-table>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue';
import { message } from 'ant-design-vue';
import { listApi } from '/@/api/suanfa';

// 表格列配置
const columns = reactive([
  { title: '姓名', dataIndex: 'name', key: 'name' },
  { title: '学号', dataIndex: 'student_id', key: 'student_id' },
  { title: '联系方式', dataIndex: 'contact', key: 'contact' },
  { title: '权重值', dataIndex: 'value', key: 'value' },
]);

// 页面数据
const data = reactive({
  userList: [] as any[],      // 通过名单
  unselectedList: [] as any[], // 未通过名单
  loading: false,
  pageSize: 10,
});

// 获取数据方法
const getDataList = async () => {
  data.loading = true;
  try {
    const response = await listApi();
    console.debug('API响应数据:', response);

    // 数据格式校验
    if (!response?.data || typeof response.data !== 'object') {
      throw new Error('无效的响应格式');
    }

    const resultData = response.data;

    // 处理selected数据
    data.userList = (resultData.selected || []).map(item => ({
      name: item.name || '未知',
      student_id: item.student_id || '无',
      contact: item.contact || '未提供',
      value: item.value || '0.00'
    }));

    // 处理unselected数据
    data.unselectedList = (resultData.unselected || []).map(item => ({
      name: item.name || '未知',
      student_id: item.student_id || '无',
      contact: item.contact || '未提供',
      value: item.value || '0.00'
    }));

    message.success(`已处理并验证 ${data.userList.length + data.unselectedList.length} 条申请记录`);

  } catch (err: any) {
    console.error('[ERROR] 请求异常:', err);
    message.error({
      content: `计算超时，请重试: ${err.message}`,
      duration: 3
    });
  } finally {
    data.loading = false;
  }
};
</script>

<style scoped lang="less">
.page-view {
  min-height: 100%;
  background: #fff;
  padding: 24px;
  display: flex;
  flex-direction: column;
}

.table-operations {
  margin-bottom: 16px;
  text-align: right;
}

.table-operations > button {
  margin-right: 8px;
}

</style>
