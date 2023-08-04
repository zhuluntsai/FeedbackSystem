import UnityEngine

def get_distance():
    objects_list = UnityEngine.Object.FindObjectsOfType(UnityEngine.GameObject)
    targets_list = ['Cube1', 'Cube2']
    target_object_list = []

    for o in objects_list:
        if o.name in targets_list:
            target_object_list.append(o.transform.position)

    Distance = UnityEngine.Vector3.Distance(target_object_list[0], target_object_list[1])
    if Distance < 3:
        UnityEngine.Debug.Log(f'Distance: {Distance}')
