param
(
    [Parameter (Mandatory = $false)]
    [object] $WebhookData
)

if ($WebhookData) {
    try
    {
        "Logging in to Azure..."
        Connect-AzAccount -Identity
    }
    catch {
        Write-Error -Message $_.Exception
        throw $_.Exception
    }
    $Body = ConvertFrom-Json -InputObject $WebhookData.RequestBody
    if ($Body.action -eq 'queued') {
        Start-AzVM -ResourceGroupName csc440-chupacabra-proj -Name gh-actions-runner -Verbose
        Start-AzMySqlFlexibleServer -ResourceGroupName csc440-chupacabra-proj -Name csc440-chupacabra-proj -Verbose
    }
    elseif ($Body.action -eq 'completed') {
        Stop-AzVM -ResourceGroupName csc440-chupacabra-proj -Name gh-actions-runner -Force -Verbose
        Stop-AzMySqlFlexibleServer -ResourceGroupName csc440-chupacabra-proj -Name csc440-chupacabra-proj -Verbose
    }
    else {
        exit;
    }
} 
else
{
    Write-Output "Missing information";
    exit;
}
