<template>
  <div class="container">
    <div class="content-wrapper">
      <!-- 头部 -->
      <header class="header">
        <h1 class="title">助学金评定系统说明</h1>
        <div class="purpose">
          <h2>评定目的</h2>
          <p>建立科学、公平、透明的助学金评价体系，通过多维度数据分析精准识别资助对象，提升发放公平性与效率。</p>
        </div>
      </header>

      <!-- 主体内容 -->
      <main class="main-content">
        <!-- 原则板块 -->
        <section class="card principle">
          <h3><span class="icon">📌</span>评定原则</h3>
          <ul>
            <li>数据驱动决策</li>
            <li>动态权重调整</li>
            <li>隐私数据保护</li>
            <li>多维交叉验证</li>
          </ul>
        </section>

        <!-- 标准板块 -->
        <section class="card standard">
          <h3><span class="icon">📋</span>评定标准</h3>
          <div class="criteria">
            <div class="criterion">
              <div class="percentage">35%</div>
              <div class="detail">
                <h4>家庭经济</h4>
                <p>收入负债比 · 家庭成员健康</p>
              </div>
            </div>
            <!-- 其他标准同理 -->
          </div>
        </section>
      </main>

      <!-- 页脚 -->
      <footer class="footer">
        <div class="version">2024.EDU 版本</div>
        <div class="issuer">学生资助中心</div>
      </footer>
    </div>
  </div>
</template>

<style lang="less" scoped>
// 基础变量
@primary-color: #2c3e50;
@secondary-color: #3498db;
@background: #f8f9fa;
@text-primary: #2c3e50;
@text-secondary: #7f8c8d;

.container {
  min-height: 100vh;
  background: @background;
  padding: 2rem;
  font-family: 'Helvetica Neue', system-ui;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
}

// 头部样式
.header {
  text-align: center;
  margin-bottom: 3rem;

  .title {
    color: @primary-color;
    font-size: 2.5rem;
    margin-bottom: 1.5rem;
    font-weight: 500;
  }

  .purpose {
    h2 {
      color: @secondary-color;
      font-size: 1.3rem;
      margin-bottom: 1rem;
    }

    p {
      color: @text-secondary;
      line-height: 1.6;
      max-width: 800px;
      margin: 0 auto;
    }
  }
}

// 卡片通用样式
.card {
  background: white;
  border-radius: 10px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);

  h3 {
    color: @primary-color;
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.8rem;

    .icon {
      font-size: 1.2em;
    }
  }
}

// 评定原则
.principle {
  ul {
    list-style: none;
    padding: 0;
    columns: 2;

    li {
      color: @text-primary;
      padding: 0.8rem 0;
      border-bottom: 1px solid #eee;
      font-size: 1.1rem;
    }
  }
}

// 评定标准
.criteria {
  display: grid;
  gap: 1.5rem;

  .criterion {
    display: flex;
    align-items: center;
    gap: 1.5rem;

    .percentage {
      background: @secondary-color;
      color: white;
      width: 60px;
      height: 60px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.2rem;
    }

    .detail {
      h4 {
        color: @primary-color;
        margin-bottom: 0.5rem;
      }

      p {
        color: @text-secondary;
        font-size: 0.95rem;
      }
    }
  }
}

// 页脚
.footer {
  text-align: center;
  padding: 2rem 0;
  color: @text-secondary;
  border-top: 1px solid #eee;
  margin-top: 2rem;

  .version {
    margin-bottom: 0.5rem;
  }
}

@media (max-width: 768px) {
  .container {
    padding: 1rem;
  }

  .header .title {
    font-size: 2rem;
  }

  .principle ul {
    columns: 1;
  }

  .criterion {
    flex-direction: column;
    text-align: center;
  }
}
</style>