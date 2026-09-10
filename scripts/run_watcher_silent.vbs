Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
currentDir = fso.GetParentFolderName(WScript.ScriptFullName)
projectDir = fso.GetParentFolderName(currentDir)
WshShell.CurrentDirectory = projectDir

userProfile = WshShell.ExpandEnvironmentStrings("%USERPROFILE%")
uvPath = userProfile & "\.local\bin\uv.exe"

If Not fso.FileExists(uvPath) Then
    uvPath = "uv.exe"
End If

cmd = Chr(34) & uvPath & Chr(34) & " run python watch_and_sync.py"
WshShell.Run cmd, 0, False
