# Encryption and decryption functions for folders

function Encrypt-Folder {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Path,
        [Parameter(Mandatory=$true)]
        [string]$Password,
        [switch]$DeleteOriginals
    )
    
    if (-not (Test-Path $Path)) {
        Write-Error "Folder '$Path' not found!"
        return
    }
    
    $key = [System.Text.Encoding]::UTF8.GetBytes($Password.PadRight(32, ' ').Substring(0,32))
    $aes = [System.Security.Cryptography.Aes]::Create()
    $aes.Key = $key
    $aes.IV = [System.Byte[]](1..16)
    
    $files = Get-ChildItem -Path $Path -Recurse -File | Where-Object { $_.Extension -notin @('.enc', '.exe', '.dll') }
    
    foreach ($file in $files) {
        try {
            $content = [System.IO.File]::ReadAllBytes($file.FullName)
            $encryptor = $aes.CreateEncryptor()
            $encrypted = $encryptor.TransformFinalBlock($content, 0, $content.Length)
            
            $encPath = $file.FullName + ".enc"
            [System.IO.File]::WriteAllBytes($encPath, $encrypted)
            
            if ($DeleteOriginals) {
                Remove-Item $file.FullName -Force
            }
            
            Write-Host "Encrypted: $($file.Name) -> $encPath"
        }
        catch {
            Write-Warning "Failed to encrypt $($file.Name): $_"
        }
    }
    
    $aes.Dispose()
    Write-Host "Encryption complete for folder: $Path"
}

function Decrypt-Folder {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Path,
        [Parameter(Mandatory=$true)]
        [string]$Password
    )
    
    if (-not (Test-Path $Path)) {
        Write-Error "Folder '$Path' not found!"
        return
    }
    
    $key = [System.Text.Encoding]::UTF8.GetBytes($Password.PadRight(32, ' ').Substring(0,32))
    $aes = [System.Security.Cryptography.Aes]::Create()
    $aes.Key = $key
    $aes.IV = [System.Byte[]](1..16)
    
    $encFiles = Get-ChildItem -Path $Path -Recurse -File | Where-Object { $_.Extension -eq '.enc' }
    
    foreach ($encFile in $encFiles) {  # Fixed: Was '#oreach' (commented typo) – now proper foreach loop
        try {
            $encrypted = [System.IO.File]::ReadAllBytes($encFile.FullName)
            $decryptor = $aes.CreateDecryptor()
            $decrypted = $decryptor.TransformFinalBlock($encrypted, 0, $encrypted.Length)
            
            $origPath = $encFile.FullName -replace '\.enc$', ''
            [System.IO.File]::WriteAllBytes($origPath, $decrypted)
            
            Remove-Item $encFile.FullName -Force
            Write-Host "Decrypted: $($encFile.Name) -> $origPath"
        }
        catch {
            Write-Warning "Failed to decrypt $($encFile.Name): Wrong password or corrupted file."
        }
    }
    
    $aes.Dispose()
    Write-Host "Decryption complete for folder: $Path"
}