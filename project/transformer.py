def transform(values):
    arr = []

    for item in values:
        arr.append(singleTransform(item))

    return arr


def singleTransform(values):
    return {
        "id": values.id,
        "id_user": values.id_user_id,
        "project_name": values.project_name,
        "created_at": str(values.created_at),
        "updated_at": str(values.updated_at)
    }