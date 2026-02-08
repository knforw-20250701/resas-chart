<template>
    <div class="modal-overlay" @click.self="$emit('close')">
        <div class="modal-content">
            <button class="close-button" @click="$emit('close')">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                >
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
            </button>

            <h3 class="modal-title">{{ regionName }}地方の人口比率</h3>

            <div class="chart-container">
                <Pie :data="chartData" :options="chartOptions" />
            </div>

            <div class="legend-grid">
                <div
                    v-for="(item, index) in regionalData"
                    :key="item.prefCode"
                    class="legend-item"
                >
                    <span
                        class="color-box"
                        :style="{
                            backgroundColor: colors[index % colors.length],
                        }"
                    ></span>
                    <span class="pref-name">{{ item.prefName }}</span>
                    <span class="pref-percent"
                        >{{ calculatePercent(item.value) }}%</span
                    >
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { Pie } from "vue-chartjs";
import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    ArcElement,
    type ChartData,
    type ChartOptions,
} from "chart.js";
import type { PrefecturePopulation } from "@/service/estat";

ChartJS.register(Title, Tooltip, Legend, ArcElement);

const props = defineProps<{
    regionName: string;
    populations: PrefecturePopulation[];
}>();

defineEmits(["close"]);

const colors = [
    "#3b82f6",
    "#10b981",
    "#f59e0b",
    "#ef4444",
    "#8b5cf6",
    "#ec4899",
    "#06b6d4",
    "#84cc16",
    "#f97316",
    "#6366f1",
];

const regionalData = computed(() => {
    return [...props.populations].sort((a, b) => b.value - a.value);
});

const totalPopulation = computed(() => {
    return props.populations.reduce((sum, p) => sum + p.value, 0);
});

const calculatePercent = (value: number) => {
    if (totalPopulation.value === 0) return 0;
    return ((value / totalPopulation.value) * 100).toFixed(1);
};

const chartData = computed<ChartData<"pie">>(() => ({
    labels: regionalData.value.map((p) => p.prefName),
    datasets: [
        {
            data: regionalData.value.map((p) => p.value),
            backgroundColor: colors.slice(0, regionalData.value.length),
            borderWidth: 1,
        },
    ],
}));

const chartOptions: ChartOptions<"pie"> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            display: false,
        },
        tooltip: {
            callbacks: {
                label: (context) => {
                    const label = context.label || "";
                    const value = context.parsed.toLocaleString();
                    const percent = calculatePercent(
                        regionalData.value[context.dataIndex].value,
                    );
                    return `${label}: ${value}人 (${percent}%)`;
                },
            },
        },
    },
};
</script>

<style scoped lang="scss">
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: var(--z-modal);
    backdrop-filter: blur(4px);
}

.modal-content {
    background: var(--card-bg);
    border-radius: var(--radius-lg);
    padding: 2.5rem;
    width: 90%;
    max-width: 600px;
    position: relative;
    box-shadow:
        0 20px 25px -5px rgba(0, 0, 0, 0.1),
        0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.close-button {
    position: absolute;
    top: var(--spacing-lg);
    right: var(--spacing-lg);
    background: none;
    border: none;
    cursor: pointer;
    color: var(--text-muted);
    transition: color 0.2s;
    padding: var(--spacing-xs);
    display: flex;

    &:hover {
        color: var(--text-main);
    }
}

.modal-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-main);
    margin: 0 0 var(--spacing-xl) 0;
    text-align: center;
}

.chart-container {
    height: 300px;
    margin-bottom: var(--spacing-xl);
}

.legend-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: var(--spacing-md);
}

.legend-item {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    font-size: 0.875rem;
}

.color-box {
    width: 12px;
    height: 12px;
    border-radius: 3px;
    flex-shrink: 0;
}

.pref-name {
    color: var(--text-main);
    font-weight: 500;
}

.pref-percent {
    color: var(--text-muted);
    margin-left: auto;
}
</style>
