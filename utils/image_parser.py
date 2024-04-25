def flatten(image: str, target_repository, project, flatten_level):
    parts = image.split('/')

    if flatten_level == -1:
        return target_repository + '/' + project + '/' + parts[-1]
    elif flatten_level == 0:
        return target_repository + '/' + project + '/' + parts[-1]
    elif flatten_level == 1:
        return target_repository + '/' + project + '/' + parts[-1]
    elif flatten_level == 2:
        return target_repository + '/' + project + '/' + parts[-1]
    elif flatten_level == 3:
        return target_repository + '/' + project + '/' + parts[-1]
