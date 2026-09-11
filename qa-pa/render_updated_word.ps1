$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$inputFile = Join-Path $root 'deliverables\รายงาน PA 2569 ครูอนันตชัย ป1 11คน ฉบับปรับปรุง.docx'
$outputFolder = Join-Path $PSScriptRoot 'updated-render'
New-Item -ItemType Directory -Path $outputFolder -Force | Out-Null
$pdfFile = Join-Path $outputFolder 'report.pdf'
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$document = $null
try {
    $document = $word.Documents.Open($inputFile, $false, $false)
    $document.Fields.Update() | Out-Null
    foreach ($toc in $document.TablesOfContents) { $toc.Update() }
    $document.Repaginate()
    $document.Fields.Update() | Out-Null
    foreach ($toc in $document.TablesOfContents) {
        $toc.Update()
        $toc.Range.Font.Name = 'TH SarabunPSK'
        $toc.Range.Font.Size = 14
        $toc.Range.ParagraphFormat.SpaceAfter = 0
        $toc.Range.ParagraphFormat.LineSpacingRule = 0
    }
    $document.Repaginate()
    foreach ($toc in $document.TablesOfContents) { $toc.UpdatePageNumbers() }
    $document.Save()
    $document.ExportAsFixedFormat($pdfFile, 17)
    Write-Output ('Pages: ' + $document.ComputeStatistics(2))
    Write-Output ('TOC: ' + $document.TablesOfContents.Count)
    Write-Output ('PDF: ' + $pdfFile)
} finally {
    if ($document) { $document.Close(0) }
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
