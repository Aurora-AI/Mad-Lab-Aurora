$target = "L-G-0000594098-0002399301.pdf"
$roots = @(
  "C:\Users\rodri\OneDrive",
  "C:\Users\rodri\Desktop",
  "C:\Users\rodri"
)

foreach ($root in $roots) {
  if (-not (Test-Path $root)) { continue }
  $match = Get-ChildItem -Path $root -Filter $target -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
  if ($match) {
    Write-Output $match.FullName
    exit 0
  }
}

exit 1
