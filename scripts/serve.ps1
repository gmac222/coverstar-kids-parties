param(
    [int]$Port = 3000,
    [string]$Root = "$PSScriptRoot\.."
)

$listener = New-Object System.Net.HttpListener
$prefix = "http://localhost:$Port/"
$listener.Prefixes.Add($prefix)

try {
    $listener.Start()
    Write-Output "Server running at $prefix"
} catch {
    Write-Error "Failed to start listener: $_"
    exit 1
}

$mimeTypes = @{
    ".html" = "text/html; charset=utf-8"
    ".htm"  = "text/html; charset=utf-8"
    ".css"  = "text/css; charset=utf-8"
    ".js"   = "application/javascript; charset=utf-8"
    ".json" = "application/json; charset=utf-8"
    ".png"  = "image/png"
    ".jpg"  = "image/jpeg"
    ".jpeg" = "image/jpeg"
    ".gif"  = "image/gif"
    ".svg"  = "image/svg+xml"
    ".ico"  = "image/x-icon"
    ".mp4"  = "video/mp4"
    ".webm" = "video/webm"
    ".webp" = "image/webp"
    ".woff" = "font/woff"
    ".woff2"= "font/woff2"
    ".txt"  = "text/plain; charset=utf-8"
    ".xml"  = "application/xml; charset=utf-8"
}

while ($listener.IsListening) {
    try {
        $context = $listener.GetContext()
        $request = $context.Request
        $response = $context.Response

        $rawUrl = [System.Uri]::UnescapeDataString($request.Url.AbsolutePath)
        $relPath = $rawUrl.TrimStart('/')
        if ([string]::IsNullOrWhiteSpace($relPath)) {
            $relPath = "index.html"
        }

        $localPath = [System.IO.Path]::Combine($Root, $relPath.Replace('/', '\'))

        if ([System.IO.Directory]::Exists($localPath)) {
            $indexPath = [System.IO.Path]::Combine($localPath, "index.html")
            if ([System.IO.File]::Exists($indexPath)) {
                $localPath = $indexPath
            }
        }

        if ([System.IO.File]::Exists($localPath)) {
            $ext = [System.IO.Path]::GetExtension($localPath).ToLower()
            $contentType = if ($mimeTypes.ContainsKey($ext)) { $mimeTypes[$ext] } else { "application/octet-stream" }
            $response.ContentType = $contentType
            $response.StatusCode = 200

            $fileBytes = [System.IO.File]::ReadAllBytes($localPath)
            $response.ContentLength64 = $fileBytes.Length
            $response.OutputStream.Write($fileBytes, 0, $fileBytes.Length)
        } else {
            $response.StatusCode = 404
            $notFoundPath = [System.IO.Path]::Combine($Root, "404.html")
            if ([System.IO.File]::Exists($notFoundPath)) {
                $response.ContentType = "text/html; charset=utf-8"
                $fileBytes = [System.IO.File]::ReadAllBytes($notFoundPath)
                $response.ContentLength64 = $fileBytes.Length
                $response.OutputStream.Write($fileBytes, 0, $fileBytes.Length)
            } else {
                $msg = [System.Text.Encoding]::UTF8.GetBytes("404 Not Found")
                $response.ContentLength64 = $msg.Length
                $response.OutputStream.Write($msg, 0, $msg.Length)
            }
        }
        $response.OutputStream.Close()
    } catch {
        # ignore individual request errors
    }
}
