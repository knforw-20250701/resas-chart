<template>
    <div class="layout">
        <!-- ヘッダ -->
        <header class="app-header">
            <div class="header-content">
                <h1 class="app-title">都道府県別人口(2020年)</h1>
            </div>
        </header>

        <main class="main-content">
            <div class="container">
                <!-- ローディング -->
                <div v-if="loading" class="loading-state">
                    <div class="spinner"></div>
                    <p>データを準備しています...</p>
                </div>
                <div v-else-if="error" class="error-state">
                    <p class="error-message">{{ error }}</p>
                    <p v-if="errorDetail" class="error-detail">
                        {{ errorDetail }}
                    </p>
                    <button @click="loadData" class="retry-button">
                        再試行
                    </button>
                </div>
                <template v-else>
                    <!-- 人口比較 -->
                    <section class="section">
                        <PopulationChart
                            :data="populations"
                            @select-prefecture="handleSelectPrefecture"
                        />
                    </section>
                    <!-- 人口詳細 -->
                    <section class="section">
                        <h2 class="section-title">人口詳細</h2>
                        <PrefectureGrid
                            :data="populations"
                            @select-prefecture="handleSelectPrefecture"
                        />
                    </section>
                </template>
            </div>
        </main>

        <!-- モーダル表示 -->
        <Teleport to="body">
            <Transition name="modal">
                <RegionPopup
                    v-if="showPopup"
                    :region-name="selectedRegion"
                    :populations="regionalPopulations"
                    @close="showPopup = false"
                />
            </Transition>
        </Teleport>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import PrefectureGrid from "@/components/PrefectureGrid.vue";
import PopulationChart from "@/components/PopulationChart.vue";
import RegionPopup from "@/components/RegionPopup.vue";
import {
    getPrefecturePopulation,
    getRegionName,
    REGIONS,
    type PrefecturePopulation,
} from "@/service/estat";

/** 人口データ */
const populations = ref<PrefecturePopulation[]>([]);
/** ロード中 */
const loading = ref(true);
/** エラー */
const error = ref<string | null>(null);
/** エラー詳細 */
const errorDetail = ref<string | null>(null);
/** 選択された都道府県コード */
const selectedPrefCode = ref<string | null>(null);
/** モーダル表示 */
const showPopup = ref(false);

/** 選択された都道府県名 */
const selectedRegion = computed(() => {
    if (!selectedPrefCode.value) return "";
    return getRegionName(selectedPrefCode.value);
});

/** 都道府県別人口 */
const regionalPopulations = computed(() => {
    const region = selectedRegion.value;
    if (!region) return [];

    const prefCodesInRegion = Object.entries(REGIONS)
        .filter(([_, r]) => r === region)
        .map(([code, _]) => code);

    return populations.value.filter((p) =>
        prefCodesInRegion.includes(p.prefCode),
    );
});

/** 都道府県選択ハンドラ */
const handleSelectPrefecture = (prefCode: string) => {
    selectedPrefCode.value = prefCode;
    showPopup.value = true;
};

/** データロード */
const loadData = async () => {
    loading.value = true;
    error.value = null;
    errorDetail.value = null;
    try {
        populations.value = await getPrefecturePopulation();
    } catch (e: any) {
        error.value = "データの取得に失敗しました。";
        errorDetail.value = e.message || String(e);
        console.error(e);
    } finally {
        loading.value = false;
    }
};

onMounted(() => {
    loadData();
});
</script>

<style scoped lang="scss">
.layout {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    background-color: var(--bg-color);
}

.app-header {
    background-color: var(--card-bg);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    height: 64px;
    display: flex;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: var(--z-header);
}

.header-content {
    max-width: 1200px;
    margin: 0 auto;
    width: 100%;
}

.app-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-main);
    padding: 0 var(--spacing-xl);
}

.main-content {
    flex: 1;
    padding: var(--spacing-xl) 0;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--spacing-xl);
}

.section {
    margin-bottom: 3rem;
}

.section-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #334155;
    margin-bottom: var(--spacing-xl);
}

.loading-state,
.error-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 6rem 0;
    color: var(--text-muted);
}

.error-message {
    font-weight: 600;
    color: #ef4444;
}

.error-detail {
    font-size: 0.875rem;
    margin-top: var(--spacing-xs);
    opacity: 0.8;
}

.spinner {
    width: 3rem;
    height: 3rem;
    border: 4px solid var(--border-color);
    border-top-color: var(--primary-color);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: var(--spacing-lg);
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

.retry-button {
    margin-top: var(--spacing-md);
    background-color: var(--primary-color);
    color: white;
    padding: 0.625rem 1.25rem;
    border-radius: var(--radius-sm);
    font-weight: 500;
    transition: background-color 0.2s;
    border: none;
    cursor: pointer;

    &:hover {
        background-color: var(--primary-hover);
    }
}
</style>
