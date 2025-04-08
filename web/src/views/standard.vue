<template>
  <div class="container">
    <div ref="vantaRef" class="background-canvas"></div>

    <div class="content-wrapper">
      <header class="header-section">
        <h1 class="title-gradient">助学金发放评价系统评定说明</h1>
        <div class="subtitle-box">
          <h2>评定目的</h2>
          <div class="divider"></div>
          <p class="highlight-text">为规范助学金发放流程，建立科学、公平、透明的评价体系，依托智慧校园大数据平台，结合学生客观行为数据与主观申报信息，精准识别家庭经济困难学生，杜绝“伪贫困生”现象，提升助学金发放的公平性与效率。</p>
        </div>
      </header>

      <section class="features-section">
        <div class="feature-card">
          <h3><span class="icon">🚀</span> 评定原则</h3>
          <ul class="feature-list">
            <li>数据驱动：以校园行为数据（消费、学习、生活）为基础，结合家庭经济申报信息交叉验证。</li>
            <li>动态调整：评价指标权重根据政策要求及学生群体特征动态优化。</li>
            <li>敏感数据脱敏处理，仅用于算法评分，不对外公开。</li>
            <li>多维验证：通过家庭收入、消费水平、行为活动，真实性检验等多维度交叉核验。</li>
          </ul>
        </div>

        <div class="feature-card">
          <h3><span class="icon">🔍</span> 评定标准</h3>
          <ul class="feature-list">
            <li>A[家庭经济状况35%] --> A1[收入负债比]+A2[家庭成员健康状况]</li>
            <li>B[消费行为分析25%] --> B1[日均消费水平]+B2[消费波动性]+B3[高端消费占比]+B4[恩格尔系数]</li>
            <li>C[学业表现评估20%] --> C1[GPA学术成绩]</li>
            <li>D[行为特征分析15%] --> D1[图书馆学习时长]+D2[学习持续性]+D3[假期学习天数]+D4[夜间停留时长]+D5[白天活动活跃度]</li>
            <li>E[真实性验证5%] --> E1[消费水平与申报收入匹配度]</li>
          </ul>
        </div>
      </section>

      <footer class="info-footer">
        <div class="info-item">
          <h4>系统版本</h4>
          <p>2024.EDU</p>
        </div>
        <div class="info-item">
          <h4>部署单位</h4>
          <p>学生资助中心</p>
        </div>
      </footer>
    </div>
  </div>
</template>

<script>
import * as THREE from 'three';
import GLOBE from 'vanta/src/vanta.globe';

export default {
  mounted() {
    this.vantaEffect = GLOBE({
      el: this.$refs.vantaRef,
      THREE: THREE,
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      minHeight: 200.0,
      minWidth: 200.0,
      scale: 1.0,
      scaleMobile: 1.0,
      color: 0x3a86ff,
      size: 0.5,
      backgroundColor: 0x0f172a,
      points: 8,
      spacing: 15
    });
  },
  beforeDestroy() {
    if (this.vantaEffect) this.vantaEffect.destroy();
  }
};
</script>

<style lang="less" scoped>
.container {
  position: relative;
  min-height: 100vh;
  background: linear-gradient(45deg, #0f172a 30%, #1e293b);
}

.background-canvas {
  position: fixed;
  width: 100%;
  height: 100vh;
  opacity: 0.4;
}

.content-wrapper {
  position: relative;
  max-width: 1200px;
  margin: 0 auto;
  padding: 4rem 2rem;
  color: #f8fafc;
}

.header-section {
  text-align: center;
  margin-bottom: 4rem;

  .title-gradient {
    font-size: 3.5rem;
    background: linear-gradient(45deg, #3b82f6, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.05em;
    margin-bottom: 1.5rem;
  }

  .subtitle-box {
    background: rgba(30, 41, 59, 0.6);
    padding: 1.5rem;
    border-radius: 1rem;
    backdrop-filter: blur(10px);

    h2 {
      font-size: 1.8rem;
      color: #94a3b8;
      margin-bottom: 1rem;
    }

    .divider {
      width: 80px;
      height: 2px;
      background: #3b82f6;
      margin: 1rem auto;
    }

    .highlight-text {
      font-size: 1.2rem;
      color: #cbd5e1;
      letter-spacing: 0.05em;
    }
  }
}

.features-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin: 3rem 0;

  .feature-card {
    background: rgba(30, 41, 59, 0.8);
    padding: 2rem;
    border-radius: 1rem;
    border: 1px solid #334155;
    transition: transform 0.3s ease;

    &:hover {
      transform: translateY(-5px);
    }

    h3 {
      font-size: 1.5rem;
      color: #94a3b8;
      margin-bottom: 1.5rem;
      display: flex;
      align-items: center;

      .icon {
        margin-right: 0.8rem;
      }
    }

    .feature-list {
      list-style: none;
      padding-left: 0;

      li {
        padding: 0.8rem 0;
        border-bottom: 1px solid #334155;
        font-size: 1.1rem;
        color: #cbd5e1;

        &:last-child {
          border-bottom: none;
        }
      }
    }
  }
}

.info-footer {
  display: flex;
  justify-content: center;
  gap: 4rem;
  margin-top: 4rem;

  .info-item {
    text-align: center;

    h4 {
      color: #94a3b8;
      font-size: 1.1rem;
      margin-bottom: 0.5rem;
    }

    p {
      color: #cbd5e1;
      font-size: 1.2rem;
      font-weight: 500;
    }
  }
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 2rem 1rem;
  }

  .header-section .title-gradient {
    font-size: 2.5rem;
  }

  .features-section {
    grid-template-columns: 1fr;
  }

  .info-footer {
    flex-direction: column;
    gap: 2rem;
  }
}
</style>