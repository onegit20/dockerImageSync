def flatten(image: str, target_repository, project, flatten_level):
    parts = image.split('/')

    if flatten_level == -1:
        return target_repository + '/' + project + '/' + parts[-1]  # 替换所有级
    elif flatten_level == 0:
        return target_repository + '/' + project + '/' + image  # 无替换
    elif flatten_level == 1:
        return target_repository + '/' + project + '/' + '/'.join(parts[1:])  # 替换1级
    elif flatten_level == 2:
        return target_repository + '/' + project + '/' + '/'.join(parts[2:])  # 替换2级
    elif flatten_level == 3:
        return target_repository + '/' + project + '/' + '/'.join(parts[3:])  # 替换3级
