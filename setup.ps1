$download_link = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-lgpl.zip"
$output_dirname = "ffmpeg"


Write-Host "Making sure we have the proper directory structure" -ForegroundColor Green
# If the out directory exists, delete it
if (Test-Path $output_dirname) {
    Remove-Item $output_dirname -Recurse -Force
}
# Create the out directory
mkdir $output_dirname

Write-Host "Downloading FFmpeg..." -ForegroundColor Blue -NoNewline
Write-Host " [This may take a while]" -ForegroundColor Yellow

$progressPreference = 'silentlyContinue'
Invoke-WebRequest $download_link -OutFile ffmpeg.zip
$progressPreference = 'Continue'

Write-Host "Download complete!" -ForegroundColor Green
Write-Host "Extracting FFmpeg..." -ForegroundColor Blue -NoNewline
Write-Host " [This may take a while]" -ForegroundColor Yellow

Expand-Archive ffmpeg.zip -DestinationPath .
cd ffmpeg-master-latest-win64-lgpl
mv "bin/*" "../ffmpeg"
cd ..
Write-Host "Extraction complete!, Cleaning up" -ForegroundColor Green
rm -r ffmpeg-master-latest-win64-lgpl
rm ffmpeg.zip
