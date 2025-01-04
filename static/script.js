document.addEventListener('DOMContentLoaded', () => {
    // 获取动态数据
    const riskValue = parseFloat(document.getElementById('riskValue').textContent.replace('%', ''));
    const thresholdValue = parseFloat(document.getElementById('threshold').textContent);

    // 获取图表的上下文
    const ctx = document.getElementById('riskChart').getContext('2d');

    // 初始化 Chart.js 图表
    const riskChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['预测风险', '风险阈值'],
            datasets: [{
                label: '风险分析',
                data: [riskValue, thresholdValue * 100],
                backgroundColor: ['rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)'],
                borderColor: ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });

    // 中英文切换逻辑
    const toggleButton = document.getElementById('toggleLanguage');
    const mainTitle = document.getElementById('mainTitle');
    const resultTitle = document.getElementById('resultTitle');
    const riskPercentageLabel = document.getElementById('riskPercentageLabel');
    const riskLevelLabel = document.getElementById('riskLevelLabel');
    const recommendationLabel = document.getElementById('recommendationLabel');
    const thresholdLabel = document.getElementById('thresholdLabel');

    toggleButton.addEventListener('click', () => {
        if (mainTitle.textContent === '风险预测结果') {
            // 切换到英文
            mainTitle.textContent = 'Risk Prediction Results';
            resultTitle.textContent = 'Prediction Results';
            riskPercentageLabel.textContent = 'Risk Percentage:';
            riskLevelLabel.textContent = 'Risk Level:';
            recommendationLabel.textContent = 'Recommendation:';
            thresholdLabel.textContent = 'Threshold:';
            toggleButton.textContent = '切换到中文 / Switch to Chinese';

            // 更新图表标签
            riskChart.data.labels = ['Risk Prediction', 'Risk Threshold'];
            riskChart.update();
        } else {
            // 切换到中文
            mainTitle.textContent = '风险预测结果';
            resultTitle.textContent = '预测结果';
            riskPercentageLabel.textContent = '风险百分比：';
            riskLevelLabel.textContent = '风险等级：';
            recommendationLabel.textContent = '建议：';
            thresholdLabel.textContent = '阈值：';
            toggleButton.textContent = '切换到英文 / Switch to English';

            // 更新图表标签
            riskChart.data.labels = ['预测风险', '风险阈值'];
            riskChart.update();
        }
    });
});