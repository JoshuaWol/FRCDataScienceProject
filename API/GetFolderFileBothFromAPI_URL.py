def getFolderFromAPI_URL (inputURL: str) ->str:
    from pathlib import Path 
    import re   
    URLAfterV3Slash = inputURL.split('v3.0/')
    URLAfterV3SlashSplitList = re.split(r"[/?]",URLAfterV3Slash[1])
    ROOT = next(p for p in Path(__file__).resolve().parents if (p/".git").exists())    
    if len(URLAfterV3SlashSplitList) < 2:
        callFolder = seasonData
    else:
        callFolder = URLAfterV3SlashSplitList[1] + 'Data'
        print(URLAfterV3SlashSplitList)
    finalFolders = ROOT/ "API" / "JSON" / callFolder
    return finalFolders

def getFileNameFromAPI_URL(inputURL: str) -> str:
    URLAfterV3Slash = inputURL.split('v3.0')
    FileNameForSave = URLAfterV3Slash[1].replace('/','|') + ".json"
    return FileNameForSave

def getFolderAndFileNameFromAPI_URL(inputURL:str) -> str:
    FolderName = getFolderFromAPI_URL (inputURL)
    FileName =  getFileNameFromAPI_URL(inputURL)
    FolderAndFileName = FolderName / FileName
    return FolderAndFileName
