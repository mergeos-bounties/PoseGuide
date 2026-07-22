# PoseGuide Bounty #47 - Three Outdoor Scenes
# 自动完成脚本 (PowerShell)

Write-Host "=== PoseGuide Bounty #47 完成脚本 ===" -ForegroundColor Cyan

# 1. 进入PoseGuide仓库
Set-Location "C:\Users\Administrator\Documents\Default Project\PoseGuide"

# 2. 确保工作区干净
git status

# 3. 检出master并更新
git checkout master
git pull origin master

# 4. 创建新分支
git checkout -b bounty-47-three-outdoor-scenes

# 5. 应用补丁（请确保补丁文件在当前目录）
git apply ..\bounty-47-complete.patch

# 6. 验证新增文件
Write-Host "`n新增文件检查:" -ForegroundColor Yellow
Get-ChildItem data/scenes/*park_picnic.json, data/scenes/*urban_sunset_rooftop.json, data/scenes/*forest_mountain_stream.json -ErrorAction SilentlyContinue | ForEach-Object { Write-Host "  ✅ $($_.Name)" }

# 7. 运行测试
Write-Host "`n运行测试..." -ForegroundColor Cyan
python -m pytest -x -q
if ($LASTEXITCODE -ne 0) { Write-Host "测试失败，请检查！" -ForegroundColor Red; exit 1 }

# 8. 更新web catalog
python scripts/build-web-catalog.py

# 9. 提交更改
git add -A
git commit -m "feat(scenes): add three outdoor scenes for #47

- Add park_picnic (casual lifestyle)
- Add urban_sunset_rooftop (cityscape golden hour)
- Add forest_mountain_stream (nature hiking)
- Update web catalog

Addresses MergeOS bounty #47 (50 MRG)

Fixes #47"

# 10. 推送分支
Write-Host "`n正在推送分支..." -ForegroundColor Cyan
git push origin bounty-47-three-outdoor-scenes
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ 分支推送成功！" -ForegroundColor Green
    Write-Host "PR链接: https://github.com/mergeos-bounties/PoseGuide/compare/master...fitzerooqq:PoseGuide:bounty-47-three-outdoor-scenes" -ForegroundColor Cyan
} else {
    Write-Host "❌ 推送失败，请手动执行: git push origin bounty-47-three-outdoor-scenes" -ForegroundColor Red
}

Write-Host "`n=== 下一步 ===" -ForegroundColor Yellow
Write-Host "1. 创建PR (如果自动推送失败，使用上述链接手动创建)"
Write-Host "2. 在 https://github.com/mergeos-bounties/PoseGuide/issues/47 评论 'I claim this bounty' 并附PR链接"
Write-Host "3. 在 https://github.com/mergeos-bounties/mergeos/issues/1 登记Claim"
