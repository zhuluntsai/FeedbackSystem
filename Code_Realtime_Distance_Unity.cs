using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using UnityEditor;
using UnityEditor.Scripting.Python;
using Python.Runtime;

public class distance_realime : MonoBehaviour
{
    public GameObject Cube1;
    public GameObject Cube2;
    public float Distance;

    void Start()
    {

    }

    void Update()
    {
        Distance = Vector3.Distance(Cube1.transform.position, Cube2.transform.position);
        if(Distance <3)
        {
            Debug.Log(Distance);
        }
    }
}