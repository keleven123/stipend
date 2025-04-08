<template>
  <div>
    <!--页面区域-->
    <div class="page-view">
      <div class="table-operations">
        <a-space>
          <a-button type="primary" @click="handleAdd">提交</a-button>
          <a-button @click="handleBatchDelete">批量删除</a-button>
        </a-space>
      </div>
      <a-table
          size="middle"
          rowKey="id"
          :loading="data.loading"
          :columns="columns"
          :data-source="data.userList"
          :scroll="{ x: 'max-content' }"
          :row-selection="rowSelection"
          :pagination="{
          size: 'default',
          current: data.page,
          pageSize: data.pageSize,
          onChange: (current) => (data.page = current),
          showSizeChanger: false,
          showTotal: (total) => `共${total}条数据`,
        }"
      >
        <template #bodyCell="{ text, record, index, column }">
          <template v-if="column.key === 'operation'">
            <span>
              <a @click="handleEdit(record)">编辑</a>
              <a-divider type="vertical" />
              <a-popconfirm title="确定删除?" ok-text="是" cancel-text="否" @confirm="confirmDelete(record)">
                <a href="#">删除</a>
              </a-popconfirm>
            </span>
          </template>
        </template>
      </a-table>
    </div>

    <!--弹窗区域-->
    <div>
      <a-modal
          :visible="modal.visile"
          :forceRender="true"
          :title="modal.title"
          ok-text="确认"
          cancel-text="取消"
          @cancel="handleCancel"
          @ok="handleOk"
          width="70%"
      >
        <div>
          <a-form
            ref="myform"
            :label-col="{ style: { width: '150px' } }"
            :model="modal.form"
            :rules="modal.rules"
            layout="vertical"
            label-align="left"
            label-wrap
            :colon="false"
            :validate-on-rule-change="false"
          >
            <a-row :gutter="24">
              <a-col span="12">
                <a-form-item label="姓名" name="name" :label-col="{ span: 8 }" :wrapper-col="{ span: 16 }">
                  <a-input placeholder="请输入" v-model:value="modal.form.name" allowClear />
                </a-form-item>
              </a-col>
              <a-col span="12">
                <a-form-item label="性别" name="gender" :label-col="{ span: 8 }" :wrapper-col="{ span: 16 }">
                  <a-select placeholder="请选择" allowClear v-model:value="modal.form.gender">
                    <a-select-option key="0" value="男">男</a-select-option>
                    <a-select-option key="1" value="女">女</a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>
              <a-col span="12">
                <a-form-item label="学号" name="student_id">
                  <a-input placeholder="请输入" v-model:value="modal.form.student_id" />
                </a-form-item>
              </a-col>
              <a-col span="12">
                <a-form-item label="联系方式" name="contact">
                  <a-input placeholder="请输入手机号" v-model:value="modal.form.contact" />
                </a-form-item>
              </a-col>
              <a-col span="12">
                <a-form-item label="政治面貌" name="political_status">
                  <a-select placeholder="请选择" allowClear v-model:value="modal.form.political_status">
                  <a-select-option key="0" value="共产党员">共产党员</a-select-option>
                  <a-select-option key="1" value="共青团员">共青团员</a-select-option>
                  <a-select-option key="2" value="群众">群众</a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>
              <a-col span="12">
                <a-form-item label="社会实践经历" name="social_practice">
                  <a-input placeholder="如果无，请填无" v-model:value="modal.form.social_practice" />
                </a-form-item>
              </a-col>
              <a-col span="12">
                <a-form-item label="家庭成员信息" name="family_members">
                  <a-input placeholder="如一家几口，是否离异" v-model:value="modal.form.family_members" />
                </a-form-item>
              </a-col>
              <a-col span="12">
                <a-form-item label="家庭年收入" name="family_annual_income">
                  <a-input placeholder="请输入" v-model:value="modal.form.family_annual_income" />
                </a-form-item>
              </a-col>
              <a-col span="12">
                <a-form-item label="经济来源" name="income_source">
                  <a-input placeholder="请输入" v-model:value="modal.form.income_source" />
                </a-form-item>
              </a-col>
              <a-col span="12">
                <a-form-item label="家庭负债情况" name="family_debt">
                  <a-input placeholder="请输入" v-model:value="modal.form.family_debt" />
                </a-form-item>
              </a-col>
              <a-col span="12">
                <a-form-item label="家庭成员健康状况" name="family_health">
                  <a-select placeholder="请选择" allowClear v-model:value="modal.form.family_health">
                    <a-select-option key="0" value="重大疾病">重大疾病</a-select-option>
                    <a-select-option key="1" value="慢性病">慢性病</a-select-option>
                    <a-select-option key="2" value="健康">健康</a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>
              <a-col span="12">
                <a-form-item label="是否享受低保" name="is_low_income">
                  <a-select placeholder="请选择" allowClear v-model:value="modal.form.is_low_income">
                    <a-select-option key="0" value="是">是</a-select-option>
                    <a-select-option key="1" value="否">否</a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>
              <a-col span="12">
                <a-form-item label="突发性经济困难说明" name="emergency_situation">
                  <a-input placeholder="请输入" v-model:value="modal.form.emergency_situation" />
                </a-form-item>
              </a-col>
              <a-col span="12">
                <a-form-item label="学业成绩/GPA" name="academic_performance">
                  <a-input placeholder="请输入" v-model:value="modal.form.academic_performance" />
                </a-form-item>
              </a-col>
              <a-col span="12">
                <a-form-item label="申请理由与用途说明" name="application_reason">
                  <a-input placeholder="请输入" v-model:value="modal.form.application_reason" />
                </a-form-item>
              </a-col>
            </a-row>
          </a-form>
        </div>
      </a-modal>
    </div>
  </div>
</template>

<script setup lang="ts">
import { FormInstance, message ,} from 'ant-design-vue';
import { createApi, listApi, detailApi, deleteApi ,updateApi} from '/@/api/zxsubmit';
import type { SelectProps } from 'ant-design-vue';

const columns = reactive([
  {
    title: '序号',
    dataIndex: 'id',
    key: 'id',
  },
  {
    title: '姓名',
    dataIndex: 'name',
    key: 'name',
  },
  {
    title: '性别',
    dataIndex: 'gender',
    key: 'gender',
  },
  {
    title: '学号',
    dataIndex: 'student_id',
    key: 'student_id',
  },
  {
    title: '政治面貌',
    dataIndex: 'political_status',
    key: 'political_status',
  },
  {
    title: '联系方式',
    dataIndex: 'contact',
    key: 'contact',
  },
  {
    title: '提交时间',
    dataIndex: 'created_at',
    key: 'created_at',
  },
  {
    title: '操作',
    dataIndex: 'action',
    key: 'operation',
    align: 'center',
    fixed: 'right',
    width: 140,
  },
]);

// 页面数据
const data = reactive({
  userList: [],
  loading: false,
  currentAdminUserName: '',
  keyword: '',
  selectedRowKeys: [] as any[],
  pageSize: 10,
  page: 1,
});

// 弹窗数据源
const modal = reactive({
  visile: false,
  editFlag: false,
  title: '',
  form: {
    id: undefined,
    name:undefined,
    gender: undefined,
    teacher_name: undefined,
    student_id: undefined,
    contact: undefined,
    political_status: undefined,
    social_practice: undefined,
    family_members: undefined,
    family_annual_income: undefined,
    income_source: undefined,
    family_debt: undefined,
    family_health: undefined,
    is_low_income: undefined,
    subsidies: undefined,
    emergency_situation: undefined,
    academic_performance: undefined,
    application_reason: undefined,
  },
  rules: {
    name: [{ required: true, message: '请输入', trigger: 'change' }],
    gender: [{ required: true, message: '请输入', trigger: 'change' }],
    teacher_name: [{ required: true, message: '请输入', trigger: 'change' }],
    student_id: [{ required: true, message: '请输入', trigger: 'change' }],
    contact: [{ required: true, message: '请输入', trigger: 'change' }],
    political_status: [{ required: true, message: '请输入', trigger: 'change' }],
    social_practice: [{ required: true, message: '请输入', trigger: 'change' }],
    family_members: [{ required: true, message: '请输入', trigger: 'change' }],
    family_annual_income: [{ required: true, message: '请输入', trigger: 'change' }],
    income_source: [{ required: true, message: '请输入', trigger: 'change' }],
    family_debt: [{ required: true, message: '请输入', trigger: 'change' }],
    family_health: [{ required: true, message: '请输入', trigger: 'change' }],
    is_low_income: [{ required: true, message: '请输入', trigger: 'change' }],
    subsidies: [{ required: true, message: '请输入', trigger: 'change' }],
    emergency_situation: [{ required: true, message: '请输入', trigger: 'change' }],
    academic_performance: [{ required: true, message: '请输入', trigger: 'change' }],
    application_reason: [{ required: true, message: '请输入', trigger: 'change' }],
  },
});

const myform = ref<FormInstance>();

onMounted(() => {
  getDataList();
});

const getDataList = () => {
  data.loading = true;
  listApi({
    keyword: data.keyword,
  })
      .then((res) => {
        data.loading = false;
        console.log(res);
        res.data.forEach((item: any, index: any) => {
          item.index = index + 1;
        });
        data.userList = res.data;
      })
      .catch((err) => {
        data.loading = false;
        console.log(err);
      });
};

const rowSelection = ref({
  onChange: (selectedRowKeys: (string | number)[], selectedRows: DataItem[]) => {
    console.log(`selectedRowKeys: ${selectedRowKeys}`, 'selectedRows: ', selectedRows);
    data.selectedRowKeys = selectedRowKeys;
  },
});

const handleAdd = () => {
  resetModal();
  modal.visile = true;
  modal.editFlag = false;
  modal.title = '新增';
  // 重置
  for (const key in modal.form) {
    modal.form[key] = undefined;
  }
};
const handleEdit = (record: any) => {
  resetModal();
  modal.visile = true;
  modal.editFlag = true;
  modal.title = '编辑';
  modal.form.id = record.id;
  // 重置
  for (const key in modal.form) {
    modal.form[key] = undefined;
  }
  for (const key in record) {
    modal.form[key] = record[key];
  }
};

const confirmDelete = (record: any) => {
  console.log('delete', record);
  deleteApi({ ids: record.id })
      .then((res) => {
        getDataList();
      })
      .catch((err) => {
        message.error(err.msg || '删除失败');
      });
};

const handleBatchDelete = () => {
  console.log(data.selectedRowKeys);
  if (data.selectedRowKeys.length <= 0) {
    console.log('hello');
    message.warn('请勾选删除项');
    return;
  }
  deleteApi({ ids: data.selectedRowKeys.join(',') })
      .then((res) => {
        message.success('删除成功');
        data.selectedRowKeys = [];
        getDataList();
      })
      .catch((err) => {
        message.error(err.msg || '删除失败');
      });
};

const handleOk = () => {
  myform.value
      ?.validate()
      .then(() => {
        if (modal.editFlag) {
          updateApi({ id: modal.form.id }, modal.form)
              .then((res) => {
                message.success('修改成功');
                hideModal();
                getDataList();
              })
              .catch((err) => {
                console.log(err);
                message.error(err.msg || '操作失败');
              });
        } else {
          createApi(modal.form)
              .then((res) => {
                hideModal();
                getDataList();
              })
              .catch((err) => {
                console.log(err);
                message.error(err.msg || '操作失败');
              });
        }
      })
      .catch((err) => {
        console.log('不能为空');
      });
};

const handleCancel = () => {
  hideModal();
};

// 恢复表单初始状态
const resetModal = () => {
  myform.value?.resetFields();
};

// 关闭弹窗
const hideModal = () => {
  modal.visile = false;
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
