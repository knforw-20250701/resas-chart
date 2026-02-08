<template>
    <div class="prefecture-grid-container">
        <div class="population-grid">
            <!-- 都道府県別詳細データ -->
            <div
                v-for="pref in data"
                :key="pref.prefCode"
                class="pref-card"
                @click="$emit('selectPrefecture', pref.prefCode)"
            >
                <div class="pref-badge">{{ pref.prefCode }}</div>
                <div class="pref-info">
                    <h3 class="pref-name">{{ pref.prefName }}</h3>
                    <p class="pref-value">
                        <span class="value-number">{{
                            pref.value.toLocaleString()
                        }}</span>
                        <span class="value-unit">人</span>
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import type { PrefecturePopulation } from "@/service/estat.ts";

defineProps<{
    data: PrefecturePopulation[];
}>();

defineEmits<{
    (e: "selectPrefecture", prefCode: string): void;
}>();
</script>

<style scoped lang="scss">
.prefecture-grid-container {
    padding: var(--spacing-md) 0;
}

.population-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: var(--spacing-lg);
}

.pref-card {
    background: var(--card-bg);
    border-radius: var(--radius-md);
    padding: var(--spacing-lg);
    display: flex;
    align-items: center;
    gap: 1.25rem;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    transition:
        transform 0.2s,
        box-shadow 0.2s;
    border: 1px solid var(--border-color);
    cursor: pointer;

    &:hover {
        transform: translateY(-2px);
        box-shadow:
            0 4px 6px -1px rgba(0, 0, 0, 0.1),
            0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border-color: var(--primary-color);
    }
}

.pref-badge {
    background-color: var(--bg-color);
    color: var(--text-muted);
    font-size: 0.75rem;
    font-weight: 600;
    width: 2.5rem;
    height: 2.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: var(--radius-sm);
    flex-shrink: 0;
}

.pref-info {
    flex: 1;
}

.pref-name {
    margin: 0;
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-main);
}

.pref-value {
    margin: 0.25rem 0 0;
    color: var(--text-muted);
}

.value-number {
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--primary-color);
    margin-right: 0.25rem;
}

.value-unit {
    font-size: 0.8rem;
}
</style>
