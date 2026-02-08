import { createRouter, createWebHashHistory } from "vue-router";
import IV0001 from "@/template/IV0001.vue";

const base = import.meta.env.BASE_URL;

const router = createRouter({
    history: createWebHashHistory(base),
    routes: [
        { component: IV0001, path: "/e-stat-chart" },
        { redirect: "/e-stat-chart", path: "/" },
    ],
});

export default router;
