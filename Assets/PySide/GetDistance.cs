using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using UnityEditor.Scripting.Python;

public class GetDistance : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        Debug.Log("start");
    }

    // Update is called once per frame
    void Update()
    {
        PythonRunner.RunString(@"
            import GetDistance
            GetDistance.get_distance()"
            );     
    }
}
