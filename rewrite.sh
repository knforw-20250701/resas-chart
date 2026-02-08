#!/bin/sh
msg=$(cat)

if [ "$msg" = "docs: update README formatting" ]; then
    echo "README加筆修正"
elif [ "$msg" = "Update contributors" ]; then
    echo "コントリビューターを更新"
elif [ "$msg" = "chore: update GH Actions to v4" ]; then
    echo "GitHub Actionsをv4に更新"
elif [ "$msg" = "fix: upgrade node version to 20 for build support" ]; then
    echo "Nodeバージョンを更新"
elif [ "$msg" = "chore: inject VITE_ESTAT_API_KEY in deployment workflow" ]; then
    echo "APIキーの秘匿化"
elif [ "$msg" = "chore: ignore .env and remove it from tracking" ]; then
    echo ".envをgitignoreに追加"
else
    echo "$msg"
fi
