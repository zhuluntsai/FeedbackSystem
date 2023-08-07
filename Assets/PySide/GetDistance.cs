using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO.Ports;
using System.Threading;
using UnityEditor.Scripting.Python;

public class GetDistance : MonoBehaviour
{
    private string port = "/dev/cu.usbmodem141301";
    private int baudRate = 115200;
    private double minFreq = 10;
    private double maxFreq = 100;
    private double minDis = 10;
    private double maxDis = 100;
    private int delayFlag = 0;
    private double timeStart = 0.0;
    private double timeCurrent = 0.0;
    private double delayDesired = 0.05;

    private double slopeA;
    private double constantB;

    public GameObject Cube1;
    public GameObject Cube2;
    public float Distance;

    SerialPort sp;
    
    // Start is called before the first frame update
    void Start()
    {
        Debug.Log("start");
        sp = new SerialPort(port, baudRate);
        sp.Open();
    }

    // Update is called once per frame
    void Update()
    {
        Distance = Vector3.Distance(Cube1.transform.position, Cube2.transform.position);
        
        if (Distance <3)
        {
            Debug.Log(Distance);
            sp.Write("10");
        }
    }
}
