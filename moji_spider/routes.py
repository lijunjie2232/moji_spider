__BASE_URL__ = "https://api.mojidict.com"


__ROUTES__ = {
    # https://api.mojidict.com/parse/users/me
    "ME": f"{__BASE_URL__}/parse/users/me",
    # https://api.mojidict.com/parse/functions/fetchSharedFoldersWithType
    # 6: recommended; 4: newest; 1: official;
    "FOLDER_BY_TYPE": f"{__BASE_URL__}/parse/functions/fetchSharedFoldersWithType",
    # https://api.mojidict.com/parse/functions/folder-fetchContentWithRelatives
    # sortType: 0: default;
    "FOLDER_BY_ID": f"{__BASE_URL__}/parse/functions/folder-fetchContentWithRelatives",
}

"""
targetType:
    431: quizlet;
    1000: collection;
    102: word or grammar;
    103: sentence;
"""
