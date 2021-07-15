def transform(values):
    arr = []

    for item in values:
        arr.append(singleTransform(item))

    return arr

def transformView(values):
    arr = []

    for item in values:
        arr.append(singleTransformView(item))

    return arr


def singleTransform(values):
    return {
        "id": values.id,
        "name": values.name,
        "method": values.method,
        "status": values.status,
        "created_at": str(values.created_at)
    }

def singleTransformView(values):
    return {
        "name": values.name,
        "total": values.total,
        "tanggal": values.tanggal, 
    }