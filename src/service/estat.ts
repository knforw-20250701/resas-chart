// src/services/estat.ts
export interface PrefecturePopulation {
    prefCode: string;
    prefName: string;
    value: number;
}

export const REGIONS: Record<string, string> = {
    "01": "北海道",
    "02": "東北",
    "03": "東北",
    "04": "東北",
    "05": "東北",
    "06": "東北",
    "07": "東北",
    "08": "関東",
    "09": "関東",
    "10": "関東",
    "11": "関東",
    "12": "関東",
    "13": "関東",
    "14": "関東",
    "15": "中部",
    "16": "中部",
    "17": "中部",
    "18": "中部",
    "19": "中部",
    "20": "中部",
    "21": "中部",
    "22": "中部",
    "23": "中部",
    "24": "近畿",
    "25": "近畿",
    "26": "近畿",
    "27": "近畿",
    "28": "近畿",
    "29": "近畿",
    "30": "近畿",
    "31": "中国",
    "32": "中国",
    "33": "中国",
    "34": "中国",
    "35": "中国",
    "36": "四国",
    "37": "四国",
    "38": "四国",
    "39": "四国",
    "40": "九州",
    "41": "九州",
    "42": "九州",
    "43": "九州",
    "44": "九州",
    "45": "九州",
    "46": "九州",
    "47": "沖縄",
};

export function getRegionName(prefCode: string): string {
    return REGIONS[prefCode] || "不明";
}

const BASE_URL = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData";

export async function getPrefecturePopulation(): Promise<
    PrefecturePopulation[]
> {
    const prefectureCodes = Array.from(
        { length: 47 },
        (_, i) => (i + 1).toString().padStart(2, "0") + "000"
    ).join(",");

    const params = new URLSearchParams({
        appId: import.meta.env.VITE_ESTAT_API_KEY,
        statsDataId: "0003410379", // 国勢調査 人口、人口動態及び世帯数
        cdTime: "2020000000", // 2020年
        cdCat01: "100", // 総数
        cdTab: "020", // 人口
        cdArea: prefectureCodes, // 都道府県コード
        metaGetFlg: "Y",
        cntGetFlg: "N",
    });

    const res = await fetch(`${BASE_URL}?${params.toString()}`);

    if (!res.ok) {
        throw new Error(`Failed to fetch e-Stat data: ${res.statusText}`);
    }

    const data = await res.json();

    if (data.GET_STATS_DATA.RESULT.STATUS !== 0) {
        throw new Error(
            `e-Stat API Error: ${data.GET_STATS_DATA.RESULT.ERROR_MSG}`
        );
    }

    const valueList = data.GET_STATS_DATA.STATISTICAL_DATA.DATA_INF.VALUE;
    const classList = data.GET_STATS_DATA.STATISTICAL_DATA.CLASS_INF.CLASS_OBJ;
    const areaClasses = classList.find(
        (obj: any) => obj["@id"] === "area"
    ).CLASS;

    const result: PrefecturePopulation[] = valueList.map((item: any) => {
        const areaCode = item["@area"];
        const areaInfo = areaClasses.find((c: any) => c["@code"] === areaCode);
        return {
            prefCode: areaCode.substring(0, 2),
            prefName: areaInfo ? areaInfo["@name"] : "不明",
            value: Number(item["$"]),
        };
    });

    return result;
}
