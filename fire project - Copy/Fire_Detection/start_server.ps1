# Fire Detection System Server Starter
Write-Output "===================================="
Write-Output "    Fire Detection System Server"
Write-Output "===================================="
Write-Output ""
Write-Output "Starting Django Development Server..."
Write-Output ""

Set-Location "C:\Users\padir\OneDrive\Desktop\Fire_Detection\Fire_Detection\backend"

Write-Output "Current directory: $(Get-Location)"
Write-Output ""
Write-Output "Starting server on http://127.0.0.1:8000/"
Write-Output ""
Write-Output "===================================="
Write-Output "    Server is now running!"
Write-Output "    Access at: http://127.0.0.1:8000/"
Write-Output "    Press Ctrl+C to stop the server"
Write-Output "===================================="
Write-Output ""

python manage.py runserver
