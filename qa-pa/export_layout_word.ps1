param([Parameter(Mandatory=$true)][string]$InputFile,[Parameter(Mandatory=$true)][string]$PdfFile,[switch]$Update)
$ErrorActionPreference='Stop'
$inputPath=(Resolve-Path -LiteralPath $InputFile).Path
$outputPath=[System.IO.Path]::GetFullPath($PdfFile)
New-Item -ItemType Directory -Path (Split-Path -Parent $outputPath) -Force | Out-Null
$word=New-Object -ComObject Word.Application
$word.Visible=$false
$word.DisplayAlerts=0
$doc=$null
try {
  $doc=$word.Documents.Open($inputPath,$false,(-not $Update))
  if ($Update) {
    $doc.Fields.Update() | Out-Null
    foreach($toc in $doc.TablesOfContents){$toc.Update()}
    $doc.Repaginate()
    foreach($toc in $doc.TablesOfContents){$toc.UpdatePageNumbers()}
    $doc.Save()
  }
  $doc.ExportAsFixedFormat($outputPath,17)
  Write-Output ('Pages: '+$doc.ComputeStatistics(2))
  Write-Output $outputPath
} catch {
  Write-Output $_.Exception.Message
  Write-Output $_.ScriptStackTrace
  throw
} finally {
  if($doc){try{$doc.Close(0)}catch{}}
  try{$word.Quit()}catch{}
  [Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
