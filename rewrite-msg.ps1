$msg = [Console]::In.ReadToEnd().Trim()

$messageMap = @{
    "docs: update README formatting" = "READMEのフォーマット更新"
    "chore: ignore .env and remove it from tracking" = ".envを無視リストに追加し追跡から削除"
    "chore: inject VITE_ESTAT_API_KEY in deployment workflow" = "デプロイワークフローにVITE_ESTAT_API_KEYを注入"
    "fix: upgrade node version to 20 for build support" = "ビルドサポートのためNodeバージョンを20にアップグレード"
    "chore: update GH Actions to v4" = "GitHub Actionsをv4に更新"
    "Update contributors" = "コントリビューター情報を更新"
}

if ($messageMap.ContainsKey($msg)) {
    Write-Output $messageMap[$msg]
} else {
    Write-Output $msg
}
