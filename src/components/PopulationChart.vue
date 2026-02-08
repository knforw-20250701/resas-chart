<template>
    <div class="chart-card">
        <div class="chart-header">
            <h3 class="chart-title">人口比較</h3>
            <!-- ソート順 -->
            <div class="sort-controls">
                <label class="sort-label">
                    <input type="radio" v-model="sortMode" value="code" />
                    <span>標　準</span>
                </label>
                <label class="sort-label">
                    <input type="radio" v-model="sortMode" value="population" />
                    <span>人口順</span>
                </label>
            </div>
        </div>
        <!-- 人口比較（横棒グラフ） -->
        <div class="chart-wrapper">
            <Bar
                v-if="chartData.labels && chartData.labels.length"
                :data="chartData"
                :options="chartOptions"
            />
            <div v-else class="loading-placeholder">
                データを読み込んでいます...
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { Bar } from "vue-chartjs";
import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    BarElement,
    CategoryScale,
    LinearScale,
    type ChartData,
    type ChartOptions,
} from "chart.js";
import type { PrefecturePopulation } from "@/service/estat";

ChartJS.register(
    Title,
    Tooltip,
    Legend,
    BarElement,
    CategoryScale,
    LinearScale,
);

const props = defineProps<{
    data: PrefecturePopulation[];
}>();

const emit = defineEmits<{
    (e: "selectPrefecture", prefCode: string): void;
}>();

/** ソート順 */
const sortMode = ref<"code" | "population">("code");

/** ソート順に基づいたデータ */
const sortedData = computed(() => {
    const data = [...props.data];
    if (sortMode.value === "population") {
        return data.sort((a, b) => b.value - a.value);
    } else {
        return data.sort((a, b) => a.prefCode.localeCompare(b.prefCode));
    }
});

/** グラフデータ */
const chartData = computed<ChartData<"bar">>(() => ({
    labels: sortedData.value.map((p) => p.prefName),
    datasets: [
        {
            label: "人口 (人)",
            data: sortedData.value.map((p) => p.value),
            backgroundColor: "rgba(59, 130, 246, 0.8)",
            borderColor: "rgb(59, 130, 246)",
            borderWidth: 1,
            borderRadius: 2,
            hoverBackgroundColor: "rgba(59, 130, 246, 1)",
            barThickness: 16,
        },
    ],
}));

/** グラフオプション */
const chartOptions: ChartOptions<"bar"> = {
    indexAxis: "y",
    responsive: true,
    maintainAspectRatio: false,
    onClick: (_, elements) => {
        if (elements.length > 0) {
            const index = elements[0].index;
            const prefCode = sortedData.value[index].prefCode;
            emit("selectPrefecture", prefCode);
        }
    },
    plugins: {
        legend: {
            display: false,
        },
        tooltip: {
            callbacks: {
                label: (context) => {
                    const value =
                        context.parsed.x !== null
                            ? context.parsed.x.toLocaleString()
                            : "0";
                    return ` ${context.dataset.label}: ${value}人`;
                },
            },
        },
    },
    scales: {
        x: {
            beginAtZero: true,
            grid: {
                display: false,
            },
            ticks: {
                callback: (value) => {
                    return (Number(value) / 10000).toLocaleString() + "万";
                },
            },
        },
        y: {
            grid: {
                display: false,
            },
            ticks: {
                autoSkip: false,
            },
        },
    },
};
</script>

<style scoped lang="scss">
.chart-card {
    background: var(--card-bg);
    border-radius: var(--radius-md);
    padding: var(--spacing-lg);
    border: 1px solid var(--border-color);
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    margin-bottom: var(--spacing-xl);
}

.chart-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--spacing-xl);
    flex-wrap: wrap;
    gap: var(--spacing-md);
}

.chart-title {
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--text-main);
    margin: 0;
}

.sort-controls {
    display: flex;
    gap: var(--spacing-md);
    background: #f1f5f9;
    padding: 0.25rem;
    border-radius: var(--radius-sm);
}

.sort-label {
    cursor: pointer;
    display: flex;
    align-items: center;
    padding: 0.375rem 0.75rem;
    border-radius: 6px;
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--text-muted);
    transition: all 0.2s;

    input {
        display: none;
    }

    &:has(input:checked) {
        background: var(--card-bg);
        color: var(--primary-color);
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    }

    &:hover:not(:has(input:checked)) {
        color: var(--text-main);
    }
}

.chart-wrapper {
    height: 1200px;
    position: relative;
}

.loading-placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: var(--text-muted);
}
</style>
