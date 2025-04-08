<template>
  <div id="userLayout">
    <div class="user-layout-header">
      <img class="logo" :src="logoImage" alt="" />
      <span>助学金发放评价系统</span>
    </div>
    <div class="main-container">
      <div class="main">
        <div class="main_right">
          <h2 class="sys_title">账号登录</h2>
          <a-form ref="myform" layout="vertical" :model="data.loginForm" :rules="data.rules" :hideRequiredMark="true">
            <a-form-item name="username" label="账号" :colon="false">
              <a-input size="large" placeholder="请输入登录账号" v-model:value="data.loginForm.username" @pressEnter="handleSubmit" />
            </a-form-item>
            <a-form-item name="password" label="密码" :colon="false">
              <a-input
                  size="large"
                  type="password"
                  placeholder="请输入登录密码"
                  v-model:value="data.loginForm.password"
                  @pressEnter="handleSubmit"
              />
            </a-form-item>
            <div>
              <a-radio-group v-model:value="value">
                <a-radio :value="1">管理员登录</a-radio>
                <a-radio :value="2">学生登录</a-radio>
              </a-radio-group>
            </div>
            <a-form-item style="padding-top: 24px">
              <a-button class="login-button" type="primary" :loading="loginBtn" size="large" block @click="handleSubmit"> 登录 </a-button>
            </a-form-item>
          </a-form>
          <div class="error-tip"></div>
        </div>
      </div>
    </div>
    <footer class="footer">
      <div class="copyright">
        <span>© 2025 · 助学金发放评价系统 ALL RIGHTS RESERVED · RCH</span>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useUserStore } from '/@/store';
import logoImage from '/@/assets/images/k-logo.png';

const value = ref<number>(1);
const router = useRouter();
const userStore = useUserStore();

import { message } from 'ant-design-vue';

const myform = ref();

const loginBtn = ref<Boolean>(false);
const checked = ref<Boolean>(false);
const data = reactive({
  loginForm: {
    username: '',
    password: '',
  },
  rules: {
    username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
    password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  },
});

const handleSubmit = () => {
  myform.value
      ?.validate()
      .then(() => {
        handleLogin();
      })
      .catch(() => {
        message.warn('不能为空');
      });
};

const handleLogin = () => {
  userStore
      .adminLogin({
        username: data.loginForm.username,
        password: data.loginForm.password,
      })
      .then((res) => {
        loginSuccess();
      })
      .catch((err) => {
        message.warn(err.msg || '登录失败');
      });
};

const loginSuccess = () => {
  router.push({ path: '/admin' });
  message.success('登录成功！');
};
</script>

<style lang="less" scoped>
#userLayout {
  position: relative;
  height: 100vh;

  .user-layout-header {
    height: 80px;
    padding: 0 24px;
    color: fade(#000, 85%);
    font-size: 24px;
    font-weight: bold;
    line-height: 80px;
    background: rgba(240, 248, 255, 0.9) !important; /* 淡蓝色带透明度 */
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);

    .logo {
      width: 36px;
      height: 36px;
      margin-right: 16px;
      margin-top: -4px;
    }
  }

  .main-container {
    width: 100%;
    height: calc(100vh - 160px);
    background-image: url('/images/admin-login-bg.jpg');
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
    display: flex;
    justify-content: center;
    align-items: center;

    .main {
      display: flex;
      border-radius: 8px;
      overflow: hidden;
      -webkit-box-shadow: 2px 2px 6px #aaa;
      box-shadow: 2px 2px 6px #aaa;

      .main_right {
        background: #ffffff;
        padding: 24px;
        width: 420px;
        user-select: none;
        background: rgba(227, 242, 253, 0.95) !important; /* 更明显的淡蓝色 */
        border: 1px solid #b3e5fc; /* 添加淡蓝色边框 */

        .sys_title {
          font-size: 24px;
          color: fade(#000, 85%);
          font-weight: bold;
          user-select: none;
          padding-bottom: 8px;
        }

        :deep(.ant-form-item label) {
          font-weight: bold;
        }

        .flex {
          align-items: center;
          display: flex;
          justify-content: space-between;
        }

        .forget_password {
          cursor: pointer;
        }

        .login-button {
          background: linear-gradient(128deg, #00aaeb, #00c1cd 59%, #0ac2b0 100%);
        }
      }

      .error-tip {
        text-align: center;
      }
    }
  }

  .footer {
    height: 80px;
    background: rgba(240, 248, 255, 0.9) !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    /* 新增居中样式 */
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .copyright {
    /* 文字样式优化 */
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: 14px;
    color: rgba(0, 0, 0, 0.7);
    letter-spacing: 0.5px;
    text-align: center;
    line-height: 1.5;
    max-width: 80%;
  }
  .ant-input {
    background: rgba(255,255,255,0.8) !important;
    border-color: #81d4fa !important;
  }
}
</style>
