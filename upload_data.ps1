Import-Module PnP.PowerShell -DisableNameChecking

$SiteURL = "https://intel.sharepoint.com/sites/VMSPFSFSBG02_KMPTE"
$FolderSiteRelativeURL = "/sites/VMSPFSFSBG02_KMPTE/Shared Documents/MVT_PHI_Report_Mgm_Report"
$Username = "wei.keong.tan@intel.com"
$Password = ConvertTo-SecureString "Elon@369" -AsPlainText -Force

$Credentials = New-Object System.Management.Automation.PSCredential($Username, $Password)

$LocalFolderPath = "C:\ScheduleTask\MVT_PHI_HVM_PBI\data"

#Connect SharePoint
try{
	Connect-PnPOnline -Url $SiteURL -Credentials $Credentials
	Write-Host "Connected to SharePoint successfully."
}catch{
    Write-Host "Failed to connect to SharePoint. Error: $($_.Exception.Message)" -ForegroundColor Red
    return
}

#Get the folder to download
try {
	$CSVFiles = Get-ChildItem -Path $LocalFolderPath -Filter *.csv -File
	if ($CSVFiles.Count -eq 0) {
		Write-Host "No CSV files found in the specified local folder. Skipping upload process."
	} else {
		foreach ($File in $CSVFiles) {
			Add-PnPFile -Path $File.FullName -Folder $FolderSiteRelativeURL -ErrorAction Stop
			#Write-Host "Uploaded $($File.Name) to SharePoint successfully."
		}
		Remove-Item -Path $CSVFiles -Force
	}
} catch {
	Write-Host "Failed to upload CSV files to SharePoint. Error: $($_.Exception.Message)" -ForegroundColor Red
}

